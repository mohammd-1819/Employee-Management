from django.db import models
# from employee.models import Employee


class Payroll(models.Model):
    employee = models.OneToOneField('employee.Employee', on_delete=models.CASCADE, related_name='payroll')
    base_salary = models.DecimalField(max_digits=10, decimal_places=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    payment_date = models.DateField()

    def __str__(self):
        return f"'{self.employee.email}' payroll"

    def total_payment(self):
        return self.base_salary + self.bonus - self.deductions
