from django.test import TestCase
from month_view.serializers import EventSerializer, DaySerializer
from month_view.models import Event
from datetime import datetime


class TestEventSerializer(TestCase):

    def setUp(self):
        self.s = EventSerializer
        self.data = {
            'title': 'test event',
            'description': 'this is a test',
            'time': f'00:00:00',
            'date': f'{datetime(2020, 5, 17).date()}'
        }

    def test_serializer_takes_valid_data(self):
        s = self.s(data=self.data)
        self.assertTrue(s.is_valid())
        instance = s.save()
        self.assertIsInstance(instance, Event)

    def test_serializer_gives_valid_data(self):
        e = Event.objects.create(title='test event', description='this is a test', time='00:00:00', date=datetime(2020, 5, 17).date())
        s = self.s(e)
        self.data['id'] = e.pk
        self.assertEqual(self.data, s.data)


class TestDaySerializer(TestCase):

    def setUp(self):
        e1 = Event.objects.create(title='event 1', description='desc for event 1', time='00:00:00', date=datetime(2020, 5, 17).date())
        e2 = Event.objects.create(title='event 2', description='desc for event 2', time='00:00:00', date=datetime(2020, 5, 18).date())
        e3 = Event.objects.create(title='event 3', description='desc for event 3', time='00:01:00', date=datetime(2020, 5, 17).date())
        e4 = Event.objects.create(title='event 4', description='desc for event 4', time='00:00:00', date=datetime(2020, 6, 17).date())


