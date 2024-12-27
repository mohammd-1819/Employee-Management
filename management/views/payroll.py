from ..models import Payroll
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from ..serializers import PayrollSerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class EmployeePayrollView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PayrollSerializer

    @extend_schema(
        tags=['Payroll'],
        summary='Employee Payroll'
    )
    def get(self, request):
        try:
            payroll = Payroll.objects.get(employee=request.user)
        except Payroll.DoesNotExist:
            return Response({'error': 'No Payroll Found For This Employee'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PayrollSerializer(instance=payroll)
        return Response(serializer.data, status=status.HTTP_200_OK)

