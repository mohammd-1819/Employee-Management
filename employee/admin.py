from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Employee


admin.site.register(Employee)
admin.site.unregister(Group)
