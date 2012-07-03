# -*- encoding:utf8 -*-
from django.contrib.auth.models import *
from django.db import models


class OwnerMixinManager(models.Manager):
    """
    Manager for multiple owner mixin
    """
    def __init__(self, owner_filter):
        super(OwnerMixinManager, self).__init__()
        self.__owner_filter = owner_filter

    def _owned_by_multi(self, users):
        user_pks = [u.pk if isinstance(u, User) else u for u in users]
        filter = {self.__owner_filter + '__in': user_pks}
        return self.filter(**filter).distinct()

    def _owned_by_single(self, user, include_staff, include_superuser):
        user_pk, user = (user.pk, user) if isinstance(user, User) else (user, None)
        if include_staff or include_superuser:
            if not user:
                user = User.objects.only('is_staff', 'is_superuser').get(pk=user_pk)
            if (include_staff and user.is_staff) or (include_superuser and user.is_superuser):
                return self.all()
        filter = {self.__owner_filter: user_pk}
        return self.filter(**filter)

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
        Is this particular model owned by a particular user.

        :user: the user object to check; this can be a ``django.contrib.auth.models.User`` instance
            or a primary key. Recommendation is to pass request.user
        :include_staff: any user who has the ``is_staff`` flag is included as an owner.
        :include_superuser: any user who has the ``is_superuser`` flag is included as an owner.
        :return: True if user has access; else False.
        """
        # Only touch elements that could cause a database operation if actually needed.
        user_pk, user = (user.pk, user) if isinstance(user, User) else (user, None)
        if include_staff or include_superuser:
            if not user:
                user = User.objects.only('is_staff', 'is_superuser').get(pk=user_pk)
            if (include_staff and user.is_staff) or (include_superuser and user.is_superuser):
                return True
        return user_pk in self.get_owner_pks()

    def is_not_owned_by(self, user, include_staff=False, include_superuser=False):
        """
        Convenience method, is an inversion of is_owned_by.
        """
        return not self.is_owned_by(user, include_staff, include_superuser)


class SingleOwnerMixin(OwnerMixinBase):
    """
    Model mixin that provides a model instance with a single owner.

    *Usage*
    ::

        class Document(SingleOwnerMixin, models.Model):
            name = models.CharField(max_length=200)
            content = models.TextField()

    """
    owner = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_owner')

    objects = OwnerMixinManager('owner')

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
    owners = models.ManyToManyField(User, related_name='%(app_label)s_%(class)s_owners')

    objects = OwnerMixinManager('owners')

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
