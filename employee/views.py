from rest_framework import status
from .models import Employee
from .serializers import SignUpSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from .pagination import Pagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, employee):
        token = super().get_token(employee)

        # Add custom claims
        token['email'] = employee.email

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignUpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    @extend_schema(
        tags=['Sign-Up'],
        responses={200: SignUpSerializer},
        auth=[]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            # Generate tokens for the user
            refresh = RefreshToken.for_user(employee)
            access = refresh.access_token

            return Response({
                'message': 'Signup Successful',
                'access_token': str(access),
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeListView(APIView, Pagination):
    permission_classes = [IsAdminUser]
    serializer_class = EmployeeSerializer

    @extend_schema(
        tags=['Employee'],
        summary='List of All Employees',
    )
    def get(self, request):
        employees = Employee.objects.all()
        result = self.paginate_queryset(employees, request)
        serializer = EmployeeSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class EmployeeDetailView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = EmployeeSerializer

    @extend_schema(
        tags=['Employee'],
        summary='Details of a Single Employee'
    )
    def get(self, request, national_code):
        try:
            employee = Employee.objects.get(national_code=national_code)
            serializer = EmployeeSerializer(instance=employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not Found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        tags=['Employee'],
        summary='Update Employee Details'
    )
    def put(self, request, national_code):
        try:
            employee = Employee.objects.get(national_code=national_code)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(instance=employee, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee Successfully Updated', 'result': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Employee'],
        summary='Delete Employee'
    )
    def delete(self, request, national_code):
        try:
            employee = Employee.objects.get(national_code=national_code)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        employee.delete()
        return Response({'message': 'Employee Deleted'}, status=status.HTTP_200_OK)


class EmployeeCreateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = EmployeeSerializer

    @extend_schema(
        tags=['Employee'],
        summary='Create New Employee (Admin Users Only)'
    )
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Employee Created Successfully", "result": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
