from django.contrib import admin
from .models import HealthInstitution

# Register your models here.
@admin.register(HealthInstitution)
class HealthInstitutionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "type",
    )
