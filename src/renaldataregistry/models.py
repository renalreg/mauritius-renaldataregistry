from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.fields import NullBooleanField
from users.models import CustomUser

# Create your models here.

# Models for registration form


class Patient(models.Model):
    TYPE_CHOICES = (
        (1, "N.I.C"),
        (2, "Passport"),
    )
    ETHNIC_CHOICES = (
        (1, "General population"),
        (2, "Hindu"),
        (3, "Islam"),
        (4, "Chinese (Buddhist)"),
        (5, "Other"),
    )
    GENDER_CHOICES = (
        (1, "Male"),
        (2, "Female"),
        (3, "Other"),
    )
    MARITALSTATUS_CHOICES = (
        (1, "Single"),
        (2, "Married (Concub...)"),
        (3, "Widow"),
        (4, "Divorced (Sep)"),
    )
    OCCUPATIONALSTATUS_CHOICES = (
        (1, "Employed"),
        (2, "Housewife"),
        (3, "Unemployed"),
        (4, "Retired"),
    )
    id = models.CharField(max_length=14, primary_key=True)
    id_type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name="Unique identifier type",
    )
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    dob = models.DateField(
        verbose_name="Date of birth",
    )
    ethnic = models.PositiveSmallIntegerField(
        choices=ETHNIC_CHOICES,
        default=1,
        verbose_name="Ethnic group",
        blank=True,
        null=True,
    )
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES,
        default=1,
        verbose_name="Gender",
        blank=True,
        null=True,
    )
    maritalstatus = models.PositiveSmallIntegerField(
        choices=MARITALSTATUS_CHOICES,
        default=1,
        verbose_name="Marital status",
        blank=True,
        null=True,
    )
    occupationalstatus = models.PositiveSmallIntegerField(
        choices=OCCUPATIONALSTATUS_CHOICES,
        default=1,
        verbose_name="Occupational status",
        blank=True,
        null=True,
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


class PatientRegistration(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    health_institution = models.ForeignKey(
        "HealthInstitution",
        on_delete=models.SET_NULL,
        verbose_name="Health institution",
        null=True,
    )
    unit = models.ForeignKey(
        "Unit",
        on_delete=models.SET_NULL,
        verbose_name="Unit",
        null=True,
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
        (0, "Unknown"),
        (1, "Public"),
        (2, "Private"),
    )
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES,
        default=0,
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

    def __str__(self):
        return self.name


class HDUnit(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="hdu_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="hdu_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RenalDiagnosis(models.Model):
    # code: ERA-EDTA CODE (4 digits code)
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


class Comorbidity(models.Model):
    comorbidity = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="co_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="co_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comorbidity


class Disability(models.Model):
    disability = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="dis_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="dis_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.disability


class LaboratoryParameter(models.Model):
    parameter = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="lp_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="lp_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.parameter


class Medication(models.Model):
    TYPE_CHOICES = (
        (1, "ESA dose"),
        (2, "IV iron dose"),
        (3, "Anti-diabetics Y/N"),
        (4, "Antihypertensives Y/N"),
    )
    medication = models.CharField(max_length=100)
    type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name="Medication type",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="m_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="m_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.medication


class PatientOccupation(models.Model):
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    occupation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
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
    # phone (P), mobile (M), email (E)
    contactchannel = models.CharField(max_length=1)
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    contactvalue = models.CharField(max_length=100, blank=True, null=True)
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
    MEASURETYPE_CHOICES = (
        (1, "Height (cm)"),
        (2, "Weight (kg)"),
        (3, "Birth weight (kg)"),
    )
    measurementtype = models.PositiveSmallIntegerField(
        choices=MEASURETYPE_CHOICES,
        default=1,
        verbose_name="Measurement type",
    )
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    measurementvalue = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
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


class PatientKRTModality(models.Model):
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    MOD_CHOICES = (
        (1, "None"),
        (2, "NK"),
        (3, "HD"),
        (4, "PD"),
        (5, "TX"),
    )
    INITIALACCESS_CHOICES = (
        (0, "Unknown"),
        (1, "AVF"),
        (2, "AVG"),
        (3, "TC"),
        (4, "NTC"),
    )
    NTCREASON_CHOICES = (
        (0, "Unknown"),
        (1, "AVF/G not ready"),
        (2, "AVF/G dysfunction"),
        (3, "On waiting list"),
        (4, "No veins"),
        (5, "Patient choice"),
    )
    modality = models.PositiveSmallIntegerField(
        choices=MOD_CHOICES,
        default=1,
        verbose_name="KRT modality",
    )
    is_first = models.BooleanField(
        default=False,
        blank=True,
        null=True,
    )
    is_current = models.BooleanField(
        default=False,
        blank=True,
        null=True,
    )
    start_date = models.DateField(
        verbose_name="Date started",
        blank=True,
        null=True,
    )
    # if patient in HD:
    hd_unit = models.ForeignKey(
        "HDUnit",
        on_delete=models.SET_NULL,
        verbose_name="HD unit",
        blank=True,
        null=True,
    )
    hd_initialaccess = models.PositiveSmallIntegerField(
        choices=INITIALACCESS_CHOICES,
        default=0,
        verbose_name="If HD was the first KRT, what was the initial access?",
    )
    hd_sessions = models.PositiveSmallIntegerField(blank=True, null=True)
    hd_minssessions = models.PositiveSmallIntegerField(blank=True, null=True)
    hd_adequacy_urr = models.DecimalField(
        verbose_name="URR %",
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
    )
    hd_adequacy_kt = models.DecimalField(
        verbose_name="Kt/v",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    hd_ntcreason = models.PositiveSmallIntegerField(
        choices=NTCREASON_CHOICES,
        default=0,
        verbose_name="If on NTC, why?",
    )
    # if patient in PD:
    pd_exchangesday = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    pd_fluidlitresday = models.DecimalField(
        verbose_name="Fluid litres/day",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    pd_adequacy = models.DecimalField(
        verbose_name="Kt/V urea",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    pd_bp = models.DecimalField(
        verbose_name="BP in mmHg",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )


class PatientAKImeasurement(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    creatinine = models.DecimalField(
        verbose_name="Latest creatinine",
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )
    egfr = models.DecimalField(
        verbose_name="Latest eGFR",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    measurement_date = models.DateField(
        verbose_name="Date done",
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="paki_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="paki_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class PatientAssessment(models.Model):
    SMOKINGSTATUS_CHOICES = (
        (0, "Unknown"),
        (1, "Never smoked"),
        (2, "Smoker"),
        (3, "Stopped"),
    )
    ALCOHOLUSE_CHOICES = (
        (0, "Unknown"),
        (1, "Never"),
        (2, "Active"),
        (3, "Stopped"),
    )
    HEPATITISB_CHOICES = (
        (0, "Unknown"),
        (1, "Positive"),
        (2, "Negative"),
        (3, "Immune"),
    )
    HEPATITISC_CHOICES = (
        (0, "Unknown"),
        (1, "Positive"),
        (2, "Negative"),
        (3, "Cured"),
    )
    HIV_CHOICES = (
        (0, "Unknown"),
        (1, "Positive"),
        (2, "Negative"),
    )
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    comorbidity = models.ManyToManyField(
        Comorbidity,
        blank=True,
        verbose_name="Comorbidities",
    )
    disability = models.ManyToManyField(
        Disability,
        blank=True,
        verbose_name="Disabilities",
    )
    smokingstatus = models.PositiveSmallIntegerField(
        choices=SMOKINGSTATUS_CHOICES,
        default=0,
        verbose_name="Smoking status",
    )
    alcoholuse = models.PositiveSmallIntegerField(
        choices=ALCOHOLUSE_CHOICES,
        default=0,
        verbose_name="Alcohol use disorder",
    )
    hepatitis_b = models.PositiveSmallIntegerField(
        choices=HEPATITISB_CHOICES,
        default=0,
        verbose_name="Hepatitis B",
    )
    hepatitis_c = models.PositiveSmallIntegerField(
        choices=HEPATITISC_CHOICES,
        default=0,
        verbose_name="Hepatitis C",
    )
    hiv = models.PositiveSmallIntegerField(
        choices=HIV_CHOICES,
        default=0,
        verbose_name="HIV",
    )
    posthd_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Post HD or dry PD weight in kg",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pas_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pas_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class PatientLPAssessment(models.Model):
    assessment = models.ForeignKey(
        "PatientAssessment",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    laboratoryparameter = models.ForeignKey(
        "LaboratoryParameter",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    assessment_value = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Value",
    )

    class Meta:
        db_table = "renaldataregistry_patientassessment_lp"


class PatientMedicationAssessment(models.Model):
    assessment = models.ForeignKey(
        "PatientAssessment",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    medication = models.ForeignKey(
        "Medication",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    medication_value = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        db_table = "renaldataregistry_patientassessment_med"
