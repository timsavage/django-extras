from django import test
from django_extras.utils import humanize


class HumanizeDescribeSecondsTestCase(test.TestCase):
    def test_seconds(self):
        self.assertEqual('12s', humanize.describe_seconds(12))

    def test_minutes(self):
        self.assertEqual('12m', humanize.describe_seconds(720))

    def test_hours(self):
        self.assertEqual('12h', humanize.describe_seconds(43200))

    def test_days(self):
        self.assertEqual('5d', humanize.describe_seconds(432000))

    def test_weeks(self):
        self.assertEqual('12w', humanize.describe_seconds(7257600))

    def test_all_one(self):
        self.assertEqual('1w 1d 1h 1m 1s', humanize.describe_seconds(694861))

    def test_mix_it_up(self):
        self.assertEqual('2w 3d 14h 42s', humanize.describe_seconds(1519242))
