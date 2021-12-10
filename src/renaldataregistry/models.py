from django.db import models
from django.db.models.constraints import UniqueConstraint
from users.models import CustomUser

# Create your models here.

# Models for registration form


class PatientRegistration(models.Model):
    id = models.IntegerField(editable=False, primary_key=True)
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    health_institution = models.ForeignKey(
        "HealthInstitution",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="reg_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="reg_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class HealthInstitution(models.Model):
    TYPE_CHOICES = (
        ("A", "Public"),
        ("P", "Private"),
        ("", "Select..."),
    )
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default="",
        verbose_name="Institution type",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="hi_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="hi_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    number = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100)
    healthinstitution = models.ForeignKey(
        "HealthInstitution",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Health institution",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="u_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="u_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class RenalDiagnosis(models.Model):
    # ERA-EDTA CODE - 4 digits code
    code = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="rd_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="rd_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class Patient(models.Model):
    TYPE_CHOICES = (
        ("N", "N.I.C"),
        ("P", "Passport"),
    )
    ETHNIC_CHOICES = (
        (0, "Select..."),
        (1, "General population"),
        (2, "Hindu"),
        (3, "Islam"),
        (4, "Chinese (Buddhist)"),
        (5, "Other"),
    )
    GENDER_CHOICES = (
        (0, "Select..."),
        (1, "Male"),
        (2, "Female"),
        (3, "Other"),
    )
    MARITALSTATUS_CHOICES = (
        (0, "Select..."),
        (1, "Single"),
        (2, "Married (Concub...)"),
        (3, "Widow"),
        (4, "Divorced (Sep)"),
    )
    OCCUPATIONALSTATUS_CHOICES = (
        (0, "Select..."),
        (1, "Employed"),
        (2, "Housewife"),
        (3, "Unemployed"),
        (4, "Retired"),
    )
    id = models.CharField(max_length=8, primary_key=True)
    id_type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default="N",
        verbose_name="Unique identifier type",
    )
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    dob = models.DateField(
        verbose_name="Date of birth",
    )
    ethnic = models.PositiveSmallIntegerField(
        choices=ETHNIC_CHOICES,
        default=0,
        verbose_name="Ethnic group",
    )
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES,
        default=0,
        verbose_name="Gender",
    )
    maritalstatus = models.PositiveSmallIntegerField(
        choices=MARITALSTATUS_CHOICES,
        default=0,
        verbose_name="Marital status",
    )
    occupationalstatus = models.PositiveSmallIntegerField(
        choices=OCCUPATIONALSTATUS_CHOICES,
        default=0,
        verbose_name="Occupational status",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pat_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pat_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class PatientOccupation(models.Model):
    id = models.IntegerField(editable=False, primary_key=True)
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    occupation = models.CharField(max_length=100)
    is_current = models.BooleanField(default=False, null=False)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="po_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="po_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class PatientContact(models.Model):
    id = models.IntegerField(editable=False, primary_key=True)
    # phone (P), mobile (M), email (E)
    contactchannel = models.CharField(max_length=1)
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    contactvalue = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pco_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pco_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["contactchannel", "patient", "created_at"],
                name="unique_patient_contact",
            )
        ]


class PatientAddress(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=5, null=True, blank=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pa_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pa_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class PatientRenalDiagnosis(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    renaldiagnosis = models.ForeignKey(
        "RenalDiagnosis",
        on_delete=models.PROTECT,
        verbose_name="Primary renal diagnosis",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="prd_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="prd_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class PatientMeasurement(models.Model):
    id = models.IntegerField(editable=False, primary_key=True)
    # height (H), weight (W), birthweight (B)
    measurementtype = models.CharField(max_length=1)
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    measurementvalue = models.DecimalField(max_digits=5, decimal_places=2)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pm_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pm_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["measurementtype", "patient", "created_at"],
                name="unique_patient_measurement",
            )
        ]
