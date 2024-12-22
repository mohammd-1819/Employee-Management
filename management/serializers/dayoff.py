from rest_framework import serializers
from ..models import DayOff


class DayOfSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOff
        fields = ('employee', 'start_date', 'end_date', 'reason', 'status')
