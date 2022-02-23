# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import PatientRegistration

admin.site.register(PatientRegistration, SimpleHistoryAdmin)
