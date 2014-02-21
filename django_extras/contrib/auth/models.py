# -*- encoding:utf8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Compatibility with django 1.5 custom user models
USER_MODEL_NAME = getattr(settings, "AUTH_USER_MODEL", 'auth.User')

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User

    def get_user_model():
        return User


class OwnerMixinManager(models.Manager):
    """
    Manager for multiple owner mixin
    """
    def __init__(self, owner_filter):
        super(OwnerMixinManager, self).__init__()
        self.owner_filter = owner_filter

    def _owned_by_multi(self, users):
        UserModel = get_user_model()
        user_pks = [u.pk if isinstance(u, UserModel) else u for u in users]
        filter_ = {self.owner_filter + '__in': user_pks}
        return self.filter(**filter_).distinct()

    def _owned_by_single(self, user, include_staff, include_superuser):
        UserModel = get_user_model()
        user_pk, user = (user.pk, user) if isinstance(user, UserModel) else (user, None)
        if include_staff or include_superuser:
            if not user:
                user = UserModel.objects.only('is_staff', 'is_superuser').get(pk=user_pk)
            if (include_staff and user.is_staff) or (include_superuser and user.is_superuser):
                return self.all()
        filter_ = {self.owner_filter: user_pk}
        return self.filter(**filter_)

    def owned_by(self, user, include_staff=False, include_superuser=False):
        """
        Filter by a user(s).

        This method accepts both ``django.contrib.auth.models.User`` instances
        or user Id's, both types of value can be mixed.

        :user: user or sequence of users to also filter by. Note this requires
            use of distinct if a tuple is specified.
        :include_staff: any user who has the ``is_staff`` flag does not get
            filtered. Can only be used with a single user.
        :include_superuser: any user who has the ``is_superuser`` flag does not
            get filtered. Can only be used with a single user.
        """
        if not user:
            return []

        if isinstance(user, (list, tuple)):
            if len(user) == 1:
                # Flatten to just being a single user.
                user = user[0]
            else:
                if include_staff or include_superuser:
                    raise TypeError('Expected a User instance or int; not list or tuple.')
                return self._owned_by_multi(user)

        return self._owned_by_single(user, include_staff, include_superuser)


class OwnerMixinBase(models.Model):
    class Meta:
        abstract = True

    def get_owner_pks(self):
        """
        Get all primary keys from owners.

        This is far more efficient that loading a full user object,
         if we don't need to avoid loading full objects.

        :return: list of primary keys.
        """
        raise NotImplemented

    def is_owned_by(self, user, include_staff=False, include_superuser=False):
        """
        Is this particular user have ownership over this model.

        :user: the user object to check; this can be a ``django.contrib.auth.models.User`` instance
            or a primary key. Recommendation is to pass request.user
        :include_staff: any user who has the ``is_staff`` flag is included as an owner.
        :include_superuser: any user who has the ``is_superuser`` flag is included as an owner.
        :return: True if user has access; else False.
        """
        UserModel = get_user_model()
        # Only touch elements that could cause a database operation if actually needed.
        user_pk, user = (user.pk, user) if isinstance(user, UserModel) else (user, None)
        if include_staff or include_superuser:
            if not user:
                user = UserModel.objects.only('is_staff', 'is_superuser').get(pk=user_pk)
            if (include_staff and user.is_staff) or (include_superuser and user.is_superuser):
                return True
        return user_pk in self.get_owner_pks()

    def is_not_owned_by(self, user, include_staff=False, include_superuser=False):
        """
        Convenience method, is an inversion of is_owned_by.
        """
        return not self.is_owned_by(user, include_staff, include_superuser)


class SingleOwnerMixinManager(OwnerMixinManager):
    def __init__(self, owner_filter='owner'):
        super(SingleOwnerMixinManager, self).__init__(owner_filter)


class SingleOwnerMixin(OwnerMixinBase):
    """
    Model mixin that provides a model instance with a single owner.

    *Usage*
    ::

        class Document(SingleOwnerMixin, models.Model):
            name = models.CharField(max_length=200)
            content = models.TextField()

    """
    owner = models.ForeignKey(USER_MODEL_NAME, verbose_name=_('owner'),
                              related_name='%(app_label)s_%(class)s_owner')

    objects = SingleOwnerMixinManager()

    class Meta:
        abstract = True

    def owner_list(self):
        """
        Get all owners of this model instance.

        :return: list of ``User`` instances.
        """
        return [self.owner]

    def get_owner_pks(self):
        return [self.owner_id]


class MultipleOwnerMixinManager(OwnerMixinManager):
    def __init__(self, owner_filter='owners'):
        super(MultipleOwnerMixinManager, self).__init__(owner_filter)


class MultipleOwnerMixin(OwnerMixinBase):
    """
    Model mixin that provides a model instance with multiple owners.

    *Usage*
    ::

        class Document(MultipleOwnerMixin, models.Model):
            name = models.CharField(max_length=200)
            content = models.TextField()

    *With through class*
    ::

        class Document(MultipleOwnerMixin, models.Model):
            name = models.CharField(max_length=200)
            content = models.TextField()
            owners = models.ManyToManyField(User, through='DocumentUser')

        class DocumentUser(models.Model):
            user = models.ForeignKey(User)
            document = models.ForeignKey(Document)
            can_edit = models.BooleanField()

    """
    owners = models.ManyToManyField(USER_MODEL_NAME, verbose_name=_('owners'),
                                    related_name='%(app_label)s_%(class)s_owners')

    objects = MultipleOwnerMixinManager()

    class Meta:
        abstract = True

    def owner_list(self):
        """
        Get all owners of this model instance.

        :return: list of ``User`` instances.
        """
        return list(self.owners.all())

    def get_owner_pks(self):
        return self.owners.values_list('id', flat=True)


class ParentOwnerMixin(OwnerMixinBase):
    """
    Model mixin that provides ownership of this model that is inherited from a parent model.

    *Usage*
    ::

        class Document(ParentOwnerMixin, models.Model):
            name = models.CharField(max_length=200)
            content = models.TextField()
            folder = models.ForeignKey(Document)

            objects = OwnerMixinManager('folder')

    """
    class Meta:
        abstract = True

    def get_owner_pks(self):
        assert isinstance(self.objects, OwnerMixinManager)
        return getattr(self, self.objects.owner_filter).get_owner_pks()
