from ..models import DayOff
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from ..serializers import DayOffSerializer, DayOffStatusSerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class DayOffListView(APIView, Pagination):
    permission_classes = (IsAdminUser,)
    serializer_class = DayOffSerializer

    @extend_schema(
        tags=['Day Off'],
        summary='List of Day Off Requests'
    )
    def get(self, request):
        day_off_requests = DayOff.objects.all()
        results = self.paginate_queryset(day_off_requests, request)
        serializer = DayOffSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class DayOffRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DayOffSerializer

    @extend_schema(
        tags=['Day Off'],
        summary='Request a Day Off',
    )
    def post(self, request):
        serializer = DayOffSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Request Sent Successfully', 'result': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDayOffList(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DayOffSerializer

    @extend_schema(
        tags=['Day Off'],
        summary='List of Employee Day Off requests'
    )
    def get(self, request):
        try:
            employee_requests = DayOff.objects.filter(user=request.user)
        except:
            return Response({'error': 'No Day Off Request Found For This Employee'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DayOffSerializer(employee_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DayOffStatusView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = DayOffStatusSerializer

    @extend_schema(
        tags=['Day Off'],
        summary='Set Day Off Request Status'
    )
    def put(self, request, day_off_id):
        try:
            day_off_request = DayOff.objects.get(id=day_off_id)
        except DayOff.DoesNotExist:
            return Response({'error', 'Request Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DayOffStatusSerializer(instance=day_off_request, data=request.data, partial=True,
                                            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            if serializer.validated_data['status'] == 'Rejected':
                day_off_request.delete()
                return Response({'message': 'Request Was Declined and Deleted'}, status=status.HTTP_200_OK)

            return Response({'message': 'Request status Updated Successfully', 'result': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DayOffDeleteView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = DayOffSerializer

    @extend_schema(
        tags=['Day Off'],
        summary='Delete Day Off Request'

    )
    def delete(self, request, day_off_id):
        try:
            day_off_request = DayOff.objects.get(id=day_off_id)
        except DayOff.DoesNotExist:
            return Response({'error', 'Request Not Found'}, status=status.HTTP_404_NOT_FOUND)

        day_off_request.delete()
        return Response({'message': 'Request Removed'})
