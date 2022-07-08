"""
This file contains the essential fields and behaviours of the data to store. Each model maps to a single database table.
"""

from simple_history.models import HistoricalRecords
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from users.models import CustomUser

# pylint: disable=too-many-lines


class Patient(models.Model):
    """
    Define a patient.
    """

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
    Y_N_CHOICES = (
        ("Y", "Yes"),
        ("N", "No"),
    )
    pid = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="N.I.C no. (or passport no. for foreigners)",
    )
    id_type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name="Unique identifier type",
    )
    name = models.CharField(max_length=100, verbose_name="Other Name/s")
    surname = models.CharField(max_length=100, verbose_name="Surname")
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
        verbose_name="Occupation",
        blank=True,
        null=True,
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Height (cm)",
        blank=True,
        null=True,
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Weight (kg)",
        blank=True,
        null=True,
    )
    birth_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Birth weight (kg)",
        blank=True,
        null=True,
    )
    street = models.CharField(
        max_length=200, verbose_name="Address", null=True, blank=True
    )
    postcode = models.CharField(
        max_length=5, verbose_name="Postcode", null=True, blank=True
    )
    current_occupation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Current employment",
    )
    prev_occupation1 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Significant previous occupation 1",
    )
    prev_occupation2 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Significant previous occupation 2",
    )
    prev_occupation3 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Significant previous occupation 3",
    )
    prev_occupation4 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Significant previous occupation 4",
    )
    in_krt_modality = models.CharField(
        max_length=1,
        choices=Y_N_CHOICES,
        default="N",
        verbose_name="Is patient on Kidney Replacement Therapy (KRT)?",
    )
    landline_number = models.CharField(
        max_length=7, null=True, blank=True, verbose_name="Home phone number"
    )
    mobile_number = models.CharField(
        max_length=8, null=True, blank=True, verbose_name="Mobile phone number"
    )
    alternative_numbers = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Alternative numbers"
    )
    email = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Email"
    )
    email2 = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Alternative email"
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
    """
    Define the main relationship patient 1 -> 1 registration * -> 1 health institution
    i.e. Every patient is registered in one main health institution and
    one health institution can be linked to one or many registrations records.
    """

    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    health_institution = models.ForeignKey(
        "HealthInstitution",
        on_delete=models.CASCADE,
        verbose_name="Health institution",
    )
    unit_no1 = models.CharField(
        verbose_name="Unit number 1",
        blank=True,
        null=True,
        max_length=6,
        validators=[RegexValidator(r"^\d{1,10}$")],
    )
    unit_no2 = models.CharField(
        verbose_name="Unit number 2",
        blank=True,
        null=True,
        max_length=6,
        validators=[RegexValidator(r"^\d{1,10}$")],
    )
    unit_no3 = models.CharField(
        verbose_name="Unit number 3",
        blank=True,
        null=True,
        max_length=6,
        validators=[RegexValidator(r"^\d{1,10}$")],
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="reg_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField()
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="reg_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()


class HealthInstitution(models.Model):
    """
    Define a health institution.
    """

    TYPE_CHOICES = (
        (0, "Unknown"),
        (1, "Public"),
        (2, "Private"),
    )
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES,
        default=0,
        verbose_name="Institution type",
    )
    is_unit_required = models.BooleanField(
        default=False,
        blank=True,
        null=True,
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


class HDUnit(models.Model):
    """
    Define a HD unit.
    """

    code = models.CharField(max_length=3, unique=True)
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


class Comorbidity(models.Model):
    """
    Define a comorbidity.
    """

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
    """
    Define a disability.
    """

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


class PatientRenalDiagnosis(models.Model):
    """
    Define the relationship patient 1 -> * renal diagnosis
    Suggestion: You should have a table for renal diagnosis codes, it was originally designed that way but Mauritius requested the change to enter the renal diagnosis code in the registration form.
    """

    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    code = models.CharField(
        verbose_name="ERA-EDTA CODE",
        blank=True,
        null=True,
        max_length=4,
        validators=[RegexValidator(r"^\d{1,10}$")],
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        null=True,
    )
    is_primary_renaldiagnosis = models.BooleanField(
        default=False,
        blank=True,
        null=True,
    )


class PatientKRTModality(models.Model):
    """
    Define the main relationship patient 1 -> * KRT modalities * -> 1 HD unit
    i.e. Every patient can have multiple KRT modalities and
    one HD unit can be linked to one or many KRT modalities (dialysis modality).
    """

    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        verbose_name="Patient",
    )
    MOD_CHOICES = (
        (1, "NK"),
        (2, "HD"),
        (3, "PD"),
        (4, "TX"),
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
    BEFOREKRT_CHOICES = (
        ("U", "Unknown"),
        ("ROPD", "ROPD"),
        ("MOPD", "MOPD"),
        ("LHC", "LHC"),
        ("OTHER_DR", "Other hospital Dr"),
        ("PRIV_NEPHR", "Private Nephrologist"),
        ("OTHER_PRIV_DR", "Other private Dr"),
    )
    Y_N_CHOICES = (
        ("Y", "Yes"),
        ("N", "No"),
        ("U", "Unknown"),
    )
    UNUSEDAVFAVGREASON_CHOICES = (
        ("U", "Unknown"),
        ("NC", "Not created"),
        ("NR", "Not ready"),
        ("AF", "Already failed"),
    )
    INSERTIONTECHNIQUE_CHOICES = (
        ("U", "Unknown"),
        ("OS", "Open surgery"),
        ("L", "Laparoscopic"),
        ("P", "Percutaneous"),
    )
    modality = models.PositiveSmallIntegerField(
        choices=MOD_CHOICES,
        default=1,
        verbose_name="KRT modality",
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
        verbose_name="If HD, state HD unit",
        blank=True,
        null=True,
    )
    # hd_initialaccess is Access on first HD in KRT modality form and Access used for last dialysis in the Dialysis Assessment form
    hd_initialaccess = models.PositiveSmallIntegerField(
        choices=INITIALACCESS_CHOICES,
        default=0,
        blank=True,
    )
    hd_tc_ntc_reason = models.PositiveSmallIntegerField(
        choices=NTCREASON_CHOICES,
        default=0,
        blank=True,
        verbose_name="If on TC or NTC, why?",
    )
    before_KRT = models.CharField(
        max_length=13,
        choices=BEFOREKRT_CHOICES,
        default="U",
        blank=True,
        verbose_name="Which of the following has the patient seen in the year before starting KRT?",
    )
    ropdorprivnephr_days = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Time first seen by ROPD or private nephrologist in days before start of KRT",
    )
    hepB_vac = models.CharField(
        max_length=1,
        choices=Y_N_CHOICES,
        default="U",
        blank=True,
        verbose_name="Has the patient completed Hep B vaccination?",
    )
    delay_start = models.CharField(
        max_length=1,
        choices=Y_N_CHOICES,
        default="U",
        blank=True,
        verbose_name="Did patient delay the start of dialysis despite nephrology advice?",
    )
    delay_beforedialysis = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Delay in full days in start of dialysis",
    )
    hd_unusedavfavgreason = models.CharField(
        max_length=2,
        choices=UNUSEDAVFAVGREASON_CHOICES,
        default="U",
        blank=True,
        verbose_name="Why AVF/AVG not used to initiate HD?",
    )
    hd_privatestart = models.CharField(
        max_length=1,
        choices=Y_N_CHOICES,
        default="U",
        blank=True,
        null=True,
        verbose_name="Was HD started in private?",
    )
    pd_catheterdays = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="How early was the PD catheter inserted (whole days before first exchange)?",
    )
    pd_insertiontechnique = models.CharField(
        max_length=2,
        choices=INSERTIONTECHNIQUE_CHOICES,
        default="U",
        blank=True,
        verbose_name="PD insertion technique",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pkrt_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField()
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pkrt_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class PatientAKImeasurement(models.Model):
    """
    Define the main relationship patient 1 -> 1 AKI set of measurements (creatinine, egrf, hb)
    """

    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    creatinine = models.DecimalField(
        verbose_name="Latest creatinine (\u03BCmol/l)",
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )
    egfr = models.DecimalField(
        verbose_name="Latest eGFR (ml/min)",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    hb = models.DecimalField(
        verbose_name="Latest Hb",
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
    created_at = models.DateTimeField()
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="paki_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class PatientAssessment(models.Model):
    """
    Define the main relationship patient 1 -> * assessments * -> * comorbidities, disabilities
    i.e. A patient can have multiple assessments and one to many comorbidities and disabilities
     can appear in one or many assessments.
    """

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
        "Comorbidity",
        blank=True,
        verbose_name="Comorbidities",
    )
    disability = models.ManyToManyField(
        "Disability",
        blank=True,
        verbose_name="Disabilities",
    )
    smokingstatus = models.PositiveSmallIntegerField(
        choices=SMOKINGSTATUS_CHOICES,
        default=0,
        verbose_name="Smoking status",
    )
    clinical_frailty = models.PositiveIntegerField(
        verbose_name="Clinical frailty scale (1 to 9)",
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(9)],
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
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pas_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField()
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="pas_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class PatientDialysisAssessment(models.Model):
    """
    Define the relationship assessment 1 -> 1 dialysis assessment
    i.e. An assessment type is a dialysis assessment.
    """

    patientassessment = models.OneToOneField(
        PatientAssessment, on_delete=models.CASCADE, primary_key=True
    )
    posthd_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Post HD or dry PD weight in kg",
    )
    # if patient in hd
    hd_sessions = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Sessions/week"
    )
    hd_minssessions = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Mins/session"
    )
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
    # if patient in pd
    pd_exchangesday = models.PositiveSmallIntegerField(
        verbose_name="Exchanges/day",
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


class PatientLPAssessment(models.Model):
    """
    Define the relationship assessment 1 -> 1 assessment for the laboratory parameters
    i.e. An assessment evaluates laboratory parameters.
    """

    patientassessment = models.OneToOneField(
        PatientAssessment, on_delete=models.CASCADE, primary_key=True
    )
    hb_gdl = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Hb g/dl",
    )
    calcium = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Calcium mmol/l",
    )
    ferritin = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Ferritin ng/ml*",
    )
    albumin = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Albumin g/l",
    )
    phosphate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Phosphate mmol/l",
    )
    tsat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="TSAT %*",
    )
    bicarbonate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Bicarbonate mmol/l",
    )
    hba1c = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="HbA1C %*",
    )
    pth = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="PTH pmol/l*",
    )

    class Meta:
        db_table = "renaldataregistry_patientassessment_lp"


class PatientMedicationAssessment(models.Model):
    """
    Define the relationship assessment 1 -> 1 set of medications
    i.e. An assessment includes a list of medications.
    """

    Y_N_U_CHOICES = (
        ("Y", "Yes"),
        ("N", "No"),
        ("U", "Unknown"),
    )
    patientassessment = models.OneToOneField(
        PatientAssessment, on_delete=models.CASCADE, primary_key=True
    )
    iu_wk = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="iu/wk (short acting)",
    )
    mcg2 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="mcg/2 wk (darbo.)",
    )
    mcg4 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="mcg/4 wk (mircera)",
    )
    mg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="mg/month",
    )
    # Anti-diabetics
    insulin = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Insulin",
    )
    sulphonylureas = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Sulphonylureas",
    )
    dpp4i = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="DPP4i",
    )
    glp1a = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="GLP1A",
    )
    meglitinides = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Meglitinides",
    )
    sglt2i = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="SGLT2i",
    )
    acarbose = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Acarbose",
    )
    metformin = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Metformin",
    )
    antidiabetic_other = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Other",
    )
    # BP Drugs
    acei = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="ACEi",
    )
    arb = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="ARB",
    )
    cc_blocker = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="CC Blocker",
    )
    beta_blocker = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Beta Blocker",
    )
    alpha_blocker = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Alpha Blocker",
    )
    centrally_acting = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Centrally acting",
    )
    p_vasodilators = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="P Vasodilators",
    )
    loop_diuretics = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Loop diuretics",
    )
    mra = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="MRA",
    )
    thiazides = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Thiazides",
    )
    renin_inhibitors = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Renin Inhibitors",
    )
    bpdrugs_others = models.CharField(
        max_length=1,
        choices=Y_N_U_CHOICES,
        default="U",
        verbose_name="Others",
    )

    class Meta:
        db_table = "renaldataregistry_patientassessment_med"


class PatientStop(models.Model):
    """
    Define the main relationship patient 1 -> 1 stop dialysis form
    """

    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    ENDREASON_CHOICES = (
        ("D", "Died"),
        ("RKF", "Recovered kidney function"),
        ("DR", "Doctor’s recommendation"),
        ("LF", "Lost to follow-up"),
        ("LM", "Left Mauritius"),
        ("FC", "Patient or family choice"),
    )
    DEATHCAUSE_CHOICES = (
        ("U", "Unknown"),
        ("C", "Cardiovascular"),
        ("CV", "Cerebrovascular"),
        ("I", "Infection"),
        ("M", "Malignancy"),
        ("SD", "Stopped dialysis"),
    )
    last_dialysis_date = models.DateField(
        verbose_name="Date of last dialysis",
        blank=True,
        null=True,
    )
    stop_reason = models.CharField(
        max_length=3,
        choices=ENDREASON_CHOICES,
        default="D",
        verbose_name="Reason",
    )
    dod = models.DateField(
        verbose_name="Date of death",
        blank=True,
        null=True,
    )
    cause_of_death = models.CharField(
        max_length=2,
        choices=DEATHCAUSE_CHOICES,
        default="D",
        verbose_name="Cause of death",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="dod_created_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="dod_updated_by",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "renaldataregistry_patientendoftreatment"
