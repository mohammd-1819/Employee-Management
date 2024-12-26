from django.db import models
# from employee.models.models import Employee


class Attendance(models.Model):
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    check_in = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"'{self.employee.email}' attendance"
