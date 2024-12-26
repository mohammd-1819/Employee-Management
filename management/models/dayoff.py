from django.db import models


# from employee.models import Employee


class DayOff(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]

    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, related_name='day_off')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return f"'{self.employee.email}' day off request"
