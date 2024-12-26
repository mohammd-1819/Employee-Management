from ..models import Department
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from ..serializers import DepartmentSerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404


class DepartmentListView(APIView, Pagination):
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartmentSerializer

    @extend_schema(
        tags=['Department'],
        summary='List of all Departments'
    )
    def get(self, request):
        departments = Department.objects.all()
        result = self.paginate_queryset(departments, request)
        serializer = DepartmentSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class DepartmentCreateView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = DepartmentSerializer

    @extend_schema(
        tags=['Department'],
        summary='Add a Department'
    )
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Department Added', "result": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageDepartmentView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = DepartmentSerializer

    @extend_schema(
        tags=['Department'],
        summary='Update Department'
    )
    def put(self, request, department_name):
        department = Department.objects.get(title=department_name)
        serializer = DepartmentSerializer(instance=department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Department Updated', 'result': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Department'],
        summary='Delete Department'
    )
    def delete(self, request, department_name):
        department = Department.objects.get(title=department_name)
        department.delete()
        return Response({'message': 'Department Deleted'})
