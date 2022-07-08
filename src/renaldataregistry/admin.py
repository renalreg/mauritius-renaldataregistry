"""
This file contains the models that can be managed in the admin module of the application.
"""

# Register your models here.
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    PatientRegistration,
    Comorbidity,
    Disability,
    HealthInstitution,
    HDUnit,
)


admin.site.register(Comorbidity)
admin.site.register(Disability)
admin.site.register(HealthInstitution)
admin.site.register(HDUnit)
admin.site.register(PatientRegistration, SimpleHistoryAdmin)
