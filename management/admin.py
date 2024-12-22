from django.contrib import admin
from .models import Department, Attendance, DayOff, Position, Payroll

admin.site.register(Department)
admin.site.register(Attendance)
admin.site.register(DayOff)
admin.site.register(Position)
admin.site.register(Payroll)
