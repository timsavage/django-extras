from django import test
from django.db import models
from django.contrib.auth.models import User
from django_extras.contrib.auth.models import SingleOwnerMixin, MultipleOwnerMixin


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


class SingleOwnerTestCase(test.TransactionTestCase):
    fixtures = ['owners.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user_staff = User.objects.get(pk=3)
        self.user_super = User.objects.get(pk=4)

        SingleOwner.objects.create(name="Test 1", description="123", owner_id=1)
        SingleOwner.objects.create(name="Test 2", description="123", owner_id=2)
        SingleOwner.objects.create(name="Test 3", description="123", owner_id=3) # Staff
        SingleOwner.objects.create(name="Test 4", description="123", owner_id=4) # Superuser

    def test_user_has_access_standard(self):
        s = SingleOwner.objects.get(pk=1)
        self.assertTrue(s.user_has_access(self.user1))
        self.assertFalse(s.user_has_access(self.user2))
        self.assertFalse(s.user_has_access(self.user_staff))
        self.assertFalse(s.user_has_access(self.user_super))

    def test_user_has_access_staff(self):
        s = SingleOwner.objects.get(pk=1)
        self.assertTrue(s.user_has_access(self.user1, allow_staff=True))
        self.assertFalse(s.user_has_access(self.user2, allow_staff=True))
        self.assertTrue(s.user_has_access(self.user_staff, allow_staff=True))
        self.assertFalse(s.user_has_access(self.user_super, allow_staff=True))

    def test_user_has_access_superuser(self):
        s = SingleOwner.objects.get(pk=1)
        self.assertTrue(s.user_has_access(self.user1, allow_superuser=True))
        self.assertFalse(s.user_has_access(self.user2, allow_superuser=True))
        self.assertFalse(s.user_has_access(self.user_staff, allow_superuser=True))
        self.assertTrue(s.user_has_access(self.user_super, allow_superuser=True))

    def test_user_has_access_both(self):
        s = SingleOwner.objects.get(pk=1)
        self.assertTrue(s.user_has_access(self.user1, allow_staff=True, allow_superuser=True))
        self.assertFalse(s.user_has_access(self.user2, allow_staff=True, allow_superuser=True))
        self.assertTrue(s.user_has_access(self.user_staff, allow_staff=True, allow_superuser=True))
        self.assertTrue(s.user_has_access(self.user_super, allow_staff=True, allow_superuser=True))

    def test_user_has_access_pk_normal(self):
        s = SingleOwner.objects.get(pk=1)
        self.assertTrue(s.user_has_access(1))
        self.assertFalse(s.user_has_access(2))
        self.assertFalse(s.user_has_access(3))
        self.assertFalse(s.user_has_access(4))

    def test_user_has_access_pk_both(self):
        s = SingleOwner.objects.get(pk=1)
        self.assertTrue(s.user_has_access(1, allow_staff=True, allow_superuser=True))
        self.assertFalse(s.user_has_access(2, allow_staff=True, allow_superuser=True))
        self.assertTrue(s.user_has_access(3, allow_staff=True, allow_superuser=True))
        self.assertTrue(s.user_has_access(4, allow_staff=True, allow_superuser=True))


class MultiOwnerTestTestCase(test.TransactionTestCase):
    fixtures = ['owners.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user_staff = User.objects.get(pk=3)
        self.user_super = User.objects.get(pk=4)

        MultiOwner.objects.create(name="Test 1", description="123").owners.add(self.user1)
        MultiOwner.objects.create(name="Test 2", description="123")
        MultiOwner.objects.create(name="Test 3", description="123")
        MultiOwner.objects.create(name="Test 4", description="123")
