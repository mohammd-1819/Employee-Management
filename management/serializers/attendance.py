from rest_framework import serializers
from ..models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('employee', 'date', 'check_in', 'check_out')
