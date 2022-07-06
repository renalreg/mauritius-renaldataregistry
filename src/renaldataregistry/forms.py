"""
This file contains the forms used in the application.
"""
from django import forms
from django.forms import (
    ModelForm,
    Textarea,
)
from bootstrap_datepicker_plus.widgets import DatePickerInput  # type: ignore
from utils.mixin import (
    PatientFormValidationMixin,
    PatientAKIMeasurementFormValidationMixin,
    PatientRegistrationFormValidationMixin,
    PatientKRTModalityFormValidationMixin,
)
from .models import (
    PatientRegistration,
    Patient,
    PatientRenalDiagnosis,
    PatientKRTModality,
    PatientAKImeasurement,
    PatientAssessment,
    PatientStop,
    PatientLPAssessment,
    PatientMedicationAssessment,
    PatientDialysisAssessment,
)


class PatientRegistrationForm(PatientRegistrationFormValidationMixin):
    class Meta:
        model = PatientRegistration
        fields = ["health_institution", "unit_no1", "unit_no2", "unit_no3"]


class PatientForm(PatientFormValidationMixin):
    class Meta:
        model = Patient
        fields = [
            "pid",
            "id_type",
            "name",
            "surname",
            "dob",
            "ethnic",
            "gender",
            "maritalstatus",
            "occupationalstatus",
            "height",
            "weight",
            "birth_weight",
            "street",
            "postcode",
            "current_occupation",
            "prev_occupation1",
            "prev_occupation2",
            "prev_occupation3",
            "prev_occupation4",
            "in_krt_modality",
            "landline_number",
            "mobile_number",
            "alternative_numbers",
            "email",
            "email2",
        ]
        widgets = {
            "dob": DatePickerInput(format="%d/%m/%Y"),
        }


class PatientRenalDiagnosisForm(ModelForm):
    class Meta:
        model = PatientRenalDiagnosis
        fields = ["code", "description"]
        widgets = {
            "description": Textarea(attrs={"cols": 20, "rows": 5}),
        }


class PatientKRTModalityForm(PatientKRTModalityFormValidationMixin):
    class Meta:
        model = PatientKRTModality
        fields = [
            "modality",
            "is_current",
            "start_date",
            "hd_unit",
            "hd_initialaccess",
            "hd_tc_ntc_reason",
            "before_KRT",
            "ropdorprivnephr_days",
            "hepB_vac",
            "delay_start",
            "delay_beforedialysis",
            "hd_unusedavfavgreason",
            "hd_privatestart",
            "pd_catheterdays",
            "pd_insertiontechnique",
        ]
        widgets = {
            "start_date": DatePickerInput(format="%d/%m/%Y"),
        }
        # Remove label in order to set one when an HD modality is registered (in this case, the label is Access on first HD) and one when the patient is assessed (in this case, the label is Access used for last dialysis)
        labels = {"hd_initialaccess": ""}


class PatientAKIMeasurementForm(PatientAKIMeasurementFormValidationMixin):
    class Meta:
        model = PatientAKImeasurement
        fields = ["creatinine", "egfr", "hb", "measurement_date"]
        widgets = {
            "measurement_date": DatePickerInput(format="%d/%m/%Y"),
        }


class PatientAssessmentForm(ModelForm):
    class Meta:
        model = PatientAssessment
        fields = [
            "comorbidity",
            "disability",
            "clinical_frailty",
            "smokingstatus",
            "alcoholuse",
            "hepatitis_b",
            "hepatitis_c",
            "hiv",
        ]
        widgets = {
            "comorbidity": forms.CheckboxSelectMultiple,
            "disability": forms.CheckboxSelectMultiple,
        }


class PatientAssessmentDialysisForm(ModelForm):
    class Meta:
        model = PatientDialysisAssessment
        fields = [
            "posthd_weight",
            "hd_sessions",
            "hd_minssessions",
            "hd_adequacy_urr",
            "hd_adequacy_kt",
            "pd_exchangesday",
            "pd_fluidlitresday",
            "pd_adequacy",
            "pd_bp",
        ]


class PatientAssessmentLPForm(ModelForm):
    class Meta:
        model = PatientLPAssessment
        fields = [
            "hb_gdl",
            "calcium",
            "ferritin",
            "albumin",
            "phosphate",
            "tsat",
            "bicarbonate",
            "hba1c",
            "pth",
        ]


class PatientAssessmentMedicationForm(ModelForm):
    class Meta:
        model = PatientMedicationAssessment
        fields = [
            "iu_wk",
            "mcg2",
            "mcg4",
            "mg",
            "insulin",
            "sulphonylureas",
            "dpp4i",
            "glp1a",
            "meglitinides",
            "sglt2i",
            "acarbose",
            "metformin",
            "antidiabetic_other",
            "acei",
            "arb",
            "cc_blocker",
            "beta_blocker",
            "alpha_blocker",
            "centrally_acting",
            "p_vasodilators",
            "loop_diuretics",
            "mra",
            "thiazides",
            "renin_inhibitors",
            "bpdrugs_others",
        ]


class PatientStopForm(ModelForm):
    class Meta:
        model = PatientStop
        fields = ["last_dialysis_date", "stop_reason", "dod", "cause_of_death"]
        widgets = {
            "last_dialysis_date": DatePickerInput(format="%d/%m/%Y"),
            "dod": DatePickerInput(format="%d/%m/%Y"),
        }
