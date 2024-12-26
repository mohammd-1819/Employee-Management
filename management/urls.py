from django.urls import path
from .views import department, attendance

app_name = 'management'

urlpatterns = [
    path('department/list/', department.DepartmentListView.as_view(), name='department-list'),
    path('department/create/', department.DepartmentCreateView.as_view(), name='department-create'),
    path('department/<str:department_name>/', department.ManageDepartmentView.as_view(), name='department-manage'),

    path('attendance/register/<str:date>/', attendance.RegisterAttendanceView.as_view(), name='attendance-register')
]
