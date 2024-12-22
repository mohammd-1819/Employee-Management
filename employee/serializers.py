import re
from rest_framework import serializers
from employee.models import Employee


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = Employee
        fields = ('email', 'password', 'first_name', 'last_name', 'national_code', 'phone')

        read_only_fields = ('is_active', 'department', 'position', 'payroll', 'hire_date')

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("invalid email address")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("password must contain 8 characters")
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("password must contain both numbers and letters")
        return value

    def create(self, validated_data):
        employee = Employee(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', '')
        )
        employee.set_password(validated_data['password'])
        employee.save()
        return employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'email', 'password', 'first_name', 'last_name', 'phone', 'department', 'national_code', 'position',
            'payroll')
        read_only_date = ('is_active', 'hire_date')
