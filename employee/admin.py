from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Employee
from management.models import Payroll


class PayrollInline(admin.StackedInline):
    model = Payroll
    extra = 1


class EmployeeAdmin(admin.ModelAdmin):
    inlines = [PayrollInline]


admin.site.register(Employee, EmployeeAdmin)
admin.site.unregister(Group)
