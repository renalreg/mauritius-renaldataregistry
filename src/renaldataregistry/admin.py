# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    PatientRegistration,
    Comorbidity,
    RenalDiagnosis,
    Disability,
    HealthInstitution,
    Unit,
)


admin.site.register(Comorbidity)
admin.site.register(RenalDiagnosis)
admin.site.register(Disability)
admin.site.register(HealthInstitution)
admin.site.register(Unit)
admin.site.register(PatientRegistration, SimpleHistoryAdmin)
