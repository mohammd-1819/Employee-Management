from rest_framework import serializers
from ..models import Payroll


class PayrollSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField()

    class Meta:
        model = Payroll
        fields = ('employee', 'base_salary', 'bonus', 'deductions', 'payment_date')
