from ..models import Position
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from ..serializers import PositionSerializer, EmployeesPositionListSerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from employee.models import Employee


class PositionListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PositionSerializer

    @extend_schema(
        tags=['Position'],
        summary='List of All Positions'
    )
    def get(self, request):
        positions = Position.objects.all()
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeesPositionListView(APIView, Pagination):
    permission_classes = (IsAdminUser,)
    serializer_class = EmployeesPositionListSerializer

    @extend_schema(
        tags=['Position'],
        summary='List of All Employees in a Position'
    )
    def get(self, request, position_title):
        # check if position exists
        position_exists = Position.objects.filter(title=position_title).exists()
        if not position_exists:
            return Response(
                {"error": "Position title is invalid or does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        employees = Employee.objects.filter(position__title=position_title).select_related('position')
        result = self.paginate_queryset(employees, request)
        serializer = EmployeesPositionListSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)
