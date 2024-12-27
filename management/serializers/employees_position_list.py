from rest_framework import serializers
from employee.models import Employee


class EmployeesPositionListSerializer(serializers.ModelSerializer):
    position = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ('email', 'position')
