from rest_framework import serializers
from month_view.models import Event



class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

class DaySerializer(serializers.Serializer):

    events = EventSerializer(many=True, read_only=True)


class MonthSerializer(serializers.Serializer):

    days = DaySerializer(many=True, read_only=True)
 