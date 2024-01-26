from django.test import TestCase
from month_view.serializers import EventSerializer
from month_view.models import Event
from datetime import time, date


class TestEventSerializer(TestCase):

    def setUp(self):
        self.s = EventSerializer
        self.data = {
            'title': 'test event',
            'description': 'this is a test',
            'time': f'00:00:00',
            'date': f'{date.today()}'
        }

    def test_serializer_takes_valid_data(self):
        s = self.s(data=self.data)
        self.assertTrue(s.is_valid())
        instance = s.save()
        self.assertIsInstance(instance, Event)

    def test_serializer_gives_valid_data(self):
        e = Event.objects.create(title='test event', description='this is a test', time='00:00:00', date=date.today())
        s = self.s(e)
        self.data['id'] = e.pk
        self.assertEqual(self.data, s.data)
