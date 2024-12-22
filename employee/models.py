from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from management.models import Department, Position


class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Employees must have a valid username")

        employee = self.model(
            email=email

        )

        employee.set_password(password)
        employee.save(using=self._db)
        return employee

    def create_superuser(self, email, password=None):
        employee = self.create_user(
            email,
            password=password,
        )
        employee.is_admin = True
        employee.save(using=self._db)
        return employee


class Employee(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(verbose_name="email", unique=True, max_length=255)
    phone = models.CharField(max_length=11, unique=True)
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='employee', blank=True,
                                   null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, blank=True, null=True)
    hire_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name='admin')

    objects = EmployeeManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
