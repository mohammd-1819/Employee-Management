from django.urls import path
from .views import department, attendance, dayoff, payroll

app_name = 'management'

urlpatterns = [
    path('department/list/', department.DepartmentListView.as_view(), name='department-list'),
    path('department/create/', department.DepartmentCreateView.as_view(), name='department-create'),
    path('department/<str:department_name>/', department.ManageDepartmentView.as_view(), name='department-manage'),

    path('attendance/register/<str:date>/', attendance.RegisterAttendanceView.as_view(), name='attendance-register'),

    path('day-off/list/', dayoff.DayOffListView.as_view(), name='dayoff-list'),
    path('day-off/request/', dayoff.DayOffRequestView.as_view(), name='dayoff-request'),
    path('day-off/status/check/<int:day_off_id>/', dayoff.DayOffStatusView.as_view(), name='dayoff-status'),
    path('day-off/delete/<int:day_off_id>/', dayoff.DayOffDeleteView.as_view(), name='dayoff-delte'),
    path('day-off/employee/requests/', dayoff.EmployeeDayOffList.as_view(), name='dayoff-employee-list'),

    path('payroll/employee/', payroll.EmployeePayrollView.as_view(), name='payroll-employee')
]
