from django import test
from django.db import models
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django_extras.contrib.auth.decorators import staff_required, superuser_required
from django_extras.contrib.auth.models import SingleOwnerMixin, MultipleOwnerMixin


@staff_required
def staff_view(request, foo, bar='eek'):
    return HttpResponse('ok')

@staff_required(include_superusers=False)
def staff_only_view(request, foo, bar='eek'):
    return HttpResponse('ok')

@staff_required(raise_exception=True)
def staff_view_throw(request, foo, bar='eek'):
    return HttpResponse('ok')


class StaffRequiredTestCase(test.TestCase):
    def __init__(self, *args, **kwargs):
        super(StaffRequiredTestCase, self).__init__(*args, **kwargs)
        self.user = User()
        self.user_staff = User(is_staff=True)
        self.user_super = User(is_superuser=True)

    def create_request(self, user):
        request = HttpRequest()
        request.user = user
        request.META['SERVER_NAME'] = 'test'
        request.META['SERVER_PORT'] = 80
        return request

    def test_normal_user(self):
        request = self.create_request(self.user)
        response = staff_view(request, 123)
        self.assertEqual(response.status_code, 302)

    def test_staff_user(self):
        request = self.create_request(self.user_staff)
        response = staff_view(request, 123)
        self.assertEqual(response.status_code, 200)

    def test_super_user(self):
        request = self.create_request(self.user_super)
        response = staff_view(request, 123)
        self.assertEqual(response.status_code, 200)

    def test_staff_only(self):
        request = self.create_request(self.user_super)
        response = staff_only_view(request, 123)
        self.assertEqual(response.status_code, 302)

    def test_raise_exception(self):
        request = self.create_request(self.user)
        self.assertRaises(PermissionDenied, lambda: staff_view_throw(request, 123))


@superuser_required
def superuser_view(request, foo, bar='eek'):
    return HttpResponse()

@superuser_required(raise_exception=True)
def superuser_view_throw(request, foo, bar='eek'):
    return HttpResponse()


class SuperuserRequiredTestCase(test.TestCase):
    def __init__(self, *args, **kwargs):
        super(SuperuserRequiredTestCase, self).__init__(*args, **kwargs)
        self.user = User()
        self.user_staff = User(is_staff=True)
        self.user_super = User(is_superuser=True)

    def create_request(self, user):
        request = HttpRequest()
        request.user = user
        request.META['SERVER_NAME'] = 'test'
        request.META['SERVER_PORT'] = 80
        return request

    def test_normal_user(self):
        request = self.create_request(self.user)
        response = superuser_view(request, 123)
        self.assertEqual(response.status_code, 302)

    def test_staff_user(self):
        request = self.create_request(self.user_staff)
        response = superuser_view(request, 123)
        self.assertEqual(response.status_code, 302)

    def test_super_user(self):
        request = self.create_request(self.user_super)
        response = superuser_view(request, 123)
        self.assertEqual(response.status_code, 200)

    def test_raise_exception(self):
        request = self.create_request(self.user)
        self.assertRaises(PermissionDenied, lambda: superuser_view_throw(request, 123))


## Models required for the follow tests

class SingleOwner(SingleOwnerMixin, models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        app_label = 'auth'


class MultiOwner(MultipleOwnerMixin, models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        app_label = 'auth'


class OwnerMixinManagerTestCase(test.TransactionTestCase):
    fixtures = ['tests']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user_staff = User.objects.get(pk=3)
        self.user_super = User.objects.get(pk=4)

        MultiOwner.objects.create(name="Test 1", description="123").owners.add(self.user1)
        MultiOwner.objects.create(name="Test 2", description="123").owners.add(self.user1, self.user2)
        MultiOwner.objects.create(name="Test 3", description="123").owners.add(self.user2)

    def test_owned_by_none(self):
        actual = MultiOwner.objects.owned_by(None)
        self.assertSequenceEqual([], actual)

    def test_owned_by_user(self):
        actual = MultiOwner.objects.owned_by(self.user1).values_list('id', flat=True)
        self.assertSequenceEqual([1, 2], actual)

    def test_owned_by_user_id(self):
        actual = MultiOwner.objects.owned_by(1).values_list('id', flat=True)
        self.assertSequenceEqual([1, 2], actual)

    def test_owned_by_single_user_list(self):
        actual = MultiOwner.objects.owned_by([self.user1]).values_list('id', flat=True)
        self.assertSequenceEqual([1, 2], actual)

    def test_owned_by_multiple_users(self):
        actual = MultiOwner.objects.owned_by([self.user1, self.user2]).values_list('id', flat=True)
        self.assertSequenceEqual([1, 2, 3], actual)

    def test_owned_by_multiple_user_ids(self):
        actual = MultiOwner.objects.owned_by([1, 2]).values_list('id', flat=True)
        self.assertSequenceEqual([1, 2, 3], actual)

    def test_owned_by_include_staff(self):
        actual = MultiOwner.objects.owned_by(self.user1, include_staff=True).values_list('id', flat=True)
        self.assertSequenceEqual([1, 2], actual)

        actual = MultiOwner.objects.owned_by(self.user_staff, include_staff=True).values_list('id', flat=True)
        self.assertSequenceEqual([1, 2, 3], actual)

        actual = MultiOwner.objects.owned_by(self.user_super, include_staff=True).values_list('id', flat=True)
        self.assertSequenceEqual([], actual)

    def test_owned_by_include_super(self):
        actual = MultiOwner.objects.owned_by(self.user1, include_superuser=True).values_list('id', flat=True)
        self.assertSequenceEqual([1, 2], actual)

        actual = MultiOwner.objects.owned_by(self.user_staff, include_superuser=True).values_list('id', flat=True)
        self.assertSequenceEqual([], actual)

        actual = MultiOwner.objects.owned_by(self.user_super, include_superuser=True).values_list('id', flat=True)
        self.assertSequenceEqual([1, 2, 3], actual)

    def test_owned_by_include_either_multiple(self):
        self.assertRaises(TypeError, lambda: MultiOwner.objects.owned_by([self.user_super, self.user1], include_staff=True))

    def test_owned_by_include_either_user_id(self):
        actual = MultiOwner.objects.owned_by(1, include_staff=True).values_list('id', flat=True)
        self.assertSequenceEqual([1, 2], actual)


class OwnerMixinBaseTestCase(test.TransactionTestCase):
    fixtures = ['tests']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user_staff = User.objects.get(pk=3)
        self.user_super = User.objects.get(pk=4)

        MultiOwner.objects.create(name="Test 1", description="123").owners.add(self.user1)
        MultiOwner.objects.create(name="Test 2", description="123").owners.add(self.user1, self.user2)
        MultiOwner.objects.create(name="Test 3", description="123").owners.add(self.user2)

    def test_is_owned_by_user(self):
        self.assertTrue(MultiOwner.objects.get(pk=1).is_owned_by(self.user1))
        self.assertFalse(MultiOwner.objects.get(pk=1).is_owned_by(self.user2))

        self.assertTrue(MultiOwner.objects.get(pk=2).is_owned_by(self.user1))
        self.assertTrue(MultiOwner.objects.get(pk=2).is_owned_by(self.user2))

        self.assertFalse(MultiOwner.objects.get(pk=3).is_owned_by(self.user1))
        self.assertTrue(MultiOwner.objects.get(pk=3).is_owned_by(self.user2))

    def test_is_owned_by_user_id(self):
        self.assertTrue(MultiOwner.objects.get(pk=1).is_owned_by(1))
        self.assertFalse(MultiOwner.objects.get(pk=1).is_owned_by(2))

        self.assertTrue(MultiOwner.objects.get(pk=2).is_owned_by(1))
        self.assertTrue(MultiOwner.objects.get(pk=2).is_owned_by(2))

        self.assertFalse(MultiOwner.objects.get(pk=3).is_owned_by(1))
        self.assertTrue(MultiOwner.objects.get(pk=3).is_owned_by(2))

    def test_is_owned_by_include_staff(self):
        self.assertTrue(MultiOwner.objects.get(pk=1).is_owned_by(self.user1, include_staff=True))
        self.assertFalse(MultiOwner.objects.get(pk=1).is_owned_by(self.user2, include_staff=True))
        self.assertTrue(MultiOwner.objects.get(pk=1).is_owned_by(self.user_staff, include_staff=True))
        self.assertFalse(MultiOwner.objects.get(pk=1).is_owned_by(self.user_super, include_staff=True))

    def test_is_owned_by_include_superuser(self):
        self.assertTrue(MultiOwner.objects.get(pk=1).is_owned_by(self.user1, include_superuser=True))
        self.assertFalse(MultiOwner.objects.get(pk=1).is_owned_by(self.user2, include_superuser=True))
        self.assertFalse(MultiOwner.objects.get(pk=1).is_owned_by(self.user_staff, include_superuser=True))
        self.assertTrue(MultiOwner.objects.get(pk=1).is_owned_by(self.user_super, include_superuser=True))

    def test_is_owned_by_include_with_pk(self):
        self.assertTrue(MultiOwner.objects.get(pk=1).is_owned_by(1, include_staff=True))
        self.assertFalse(MultiOwner.objects.get(pk=1).is_owned_by(2, include_staff=True))
        self.assertTrue(MultiOwner.objects.get(pk=1).is_owned_by(3, include_staff=True))
        self.assertFalse(MultiOwner.objects.get(pk=1).is_owned_by(4, include_staff=True))


class SingleOwnerTestCase(test.TransactionTestCase):
    fixtures = ['tests']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user_staff = User.objects.get(pk=3)
        self.user_super = User.objects.get(pk=4)

        SingleOwner.objects.create(name="Test 1", description="123", owner_id=1)
        SingleOwner.objects.create(name="Test 2", description="123", owner_id=2)
        SingleOwner.objects.create(name="Test 3", description="123", owner_id=3) # Staff
        SingleOwner.objects.create(name="Test 4", description="123", owner_id=4) # Superuser

    def test_get_owner_pks(self):
        actual = SingleOwner.objects.get(pk=1).get_owner_pks()
        self.assertListEqual([1], actual)

        actual = SingleOwner.objects.get(pk=2).get_owner_pks()
        self.assertListEqual([2], actual)

    def test_get_owners_list(self):
        actual = SingleOwner.objects.get(pk=1).owner_list()
        self.assertListEqual([self.user1], actual)

        actual = SingleOwner.objects.get(pk=2).owner_list()
        self.assertListEqual([self.user2], actual)

    def test_get_related_owner(self):
        # This is a test case for
        actual = SingleOwner.objects.get(pk=1)
        owner = actual.owner
        self.assertEqual(self.user1, owner)


class MultiOwnerTestTestCase(test.TransactionTestCase):
    fixtures = ['tests']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user_staff = User.objects.get(pk=3)
        self.user_super = User.objects.get(pk=4)

        MultiOwner.objects.create(name="Test 1", description="123").owners.add(self.user1)
        MultiOwner.objects.create(name="Test 2", description="123").owners.add(self.user1, self.user2)
        MultiOwner.objects.create(name="Test 3", description="123")
        MultiOwner.objects.create(name="Test 4", description="123")

    def test_get_owner_pks(self):
        actual = MultiOwner.objects.get(pk=1).get_owner_pks()
        self.assertSequenceEqual([1], actual)

        actual = MultiOwner.objects.get(pk=2).get_owner_pks()
        self.assertSequenceEqual([1, 2], actual)

    def test_get_owners_list(self):
        actual = MultiOwner.objects.get(pk=1).owner_list()
        self.assertListEqual([self.user1], actual)

        actual = MultiOwner.objects.get(pk=2).owner_list()
        self.assertListEqual([self.user1, self.user2], actual)

    def test_get_related_owners(self):
        actual = MultiOwner.objects.get(pk=1)
        owners = list(actual.owners.all())
        self.assertEqual([self.user1], owners)
