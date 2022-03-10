# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    PatientRegistration,
    Comorbidity,
    RenalDiagnosis,
    Disability,
    LaboratoryParameter,
    Medication,
)


admin.site.register(Comorbidity)
admin.site.register(RenalDiagnosis)
admin.site.register(Disability)
admin.site.register(LaboratoryParameter)
admin.site.register(Medication)
admin.site.register(PatientRegistration, SimpleHistoryAdmin)
