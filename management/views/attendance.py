from ..models import Attendance
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.utils.timezone import now
from ..serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class RegisterAttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    @extend_schema(
        tags=['Attendance'],
        summary='Register Employee Attendance'
    )
    def post(self, request, date):
        user = request.user
        try:
            employee = user
        except AttributeError:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        # get the date from post request
        date = date

        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=date,
            defaults={'check_in': now().time()}
        )

        if not created:  # اگر قبلاً ورود ثبت شده باشد، زمان خروج را ثبت می‌کند
            if attendance.check_out:  # اگر خروج قبلاً ثبت شده باشد
                return Response({"message": "Attendance already completed for this date."},
                                status=status.HTTP_400_BAD_REQUEST)

            attendance.check_out = now().time()
            attendance.save()

        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_200_OK)
