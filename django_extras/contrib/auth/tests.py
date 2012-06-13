from django import test
from django.db import models
from django.contrib.auth.models import User
from django_extras.contrib.auth.models import SingleOwnerMixin, MultipleOwnerMixin


class SingleOwner(SingleOwnerMixin, models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class MultiOwner(MultipleOwnerMixin, models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class SingleOwnerTestCase(test.TransactionTestCase):
    fixtures = ['owners.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user_staff = User.objects.get(pk=3)
        self.user_admin = User.objects.get(pk=4)

        SingleOwner.objects.create(name="Test 1", description="123", owner_id=1)
        SingleOwner.objects.create(name="Test 2", description="123", owner_id=2)
        SingleOwner.objects.create(name="Test 3", description="123", owner_id=3) # Staff
        SingleOwner.objects.create(name="Test 4", description="123", owner_id=4) # Admin

    def testOwnedBy(self):
        s = SingleOwner.objects.get(1)
        self.assertTrue(s.owned_by(self.user1))


class MultiOwnerTestTestCase(test.TransactionTestCase):
    fixtures = ['owners.json']

