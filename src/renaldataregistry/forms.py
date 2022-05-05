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
    Unit,
    PatientRegistration,
    Patient,
    PatientRenalDiagnosis,
    PatientKRTModality,
    PatientAKImeasurement,
    PatientAssessment,
    PatientStop,
    PatientLPAssessment,
    PatientMedicationAssessment,
)


class PatientRegistrationForm(PatientRegistrationFormValidationMixin):
    class Meta:
        model = PatientRegistration
        fields = ["health_institution", "unit"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["unit"].queryset = Unit.objects.none()

        if "health_institution" in self.data:
            # post data
            try:
                hi_id = int(self.data.get("health_institution"))
                self.fields["unit"].queryset = Unit.objects.filter(
                    healthinstitution=hi_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Get units from linked to the registered hi
            self.fields[
                "unit"
            ].queryset = self.instance.health_institution.unit_set.order_by("name")


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
            "landline_number1",
            "landline_number2",
            "mobile_number1",
            "mobile_number2",
            "email",
            "email2",
        ]
        widgets = {
            "dob": DatePickerInput(format="%d/%m/%Y"),
        }


class PatientRenalDiagnosisForm(ModelForm):
    class Meta:
        model = PatientRenalDiagnosis
        fields = ["description", "renaldiagnosis"]
        widgets = {
            "description": Textarea(attrs={"cols": 20, "rows": 5}),
        }


class PatientKRTModalityForm(PatientKRTModalityFormValidationMixin):
    class Meta:
        model = PatientKRTModality
        fields = [
            "modality",
            "is_first",
            "is_current",
            "start_date",
            "hd_unit",
            "hd_initialaccess",
            "hd_sessions",
            "hd_minssessions",
            "hd_adequacy_urr",
            "hd_adequacy_kt",
            "hd_ntcreason",
            "pd_exchangesday",
            "pd_fluidlitresday",
            "pd_adequacy",
            "pd_bp",
            "before_KRT",
            "ropdorprivnephr_days",
            "hepB_vac",
            "delay_start",
            "delay_beforedialysis",
            "hd_unusedavfavgreason",
            "pd_catheterdays",
            "pd_insertiontechnique",
        ]
        widgets = {
            "start_date": DatePickerInput(format="%d/%m/%Y"),
        }


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
            "smokingstatus",
            "alcoholuse",
            "hepatitis_b",
            "hepatitis_c",
            "hiv",
            "posthd_weight",
        ]
        widgets = {
            "comorbidity": forms.CheckboxSelectMultiple,
            "disability": forms.CheckboxSelectMultiple,
        }


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
            "antidiab_others1",
            "antidiab_others2",
            "antidiab_others3",
            "acei",
            "arb",
            "cc_blocker",
            "beta_blocker",
            "alpha_blocker",
            "methyldopa",
            "antihypertensives_others1",
            "antihypertensives_others2",
            "antihypertensives_others3",
            "antihypertensives_others4",
            "antihypertensives_others5",
        ]


class PatientStopForm(ModelForm):
    class Meta:
        model = PatientStop
        fields = ["last_dialysis_date", "stop_reason", "dod", "cause_of_death"]
        widgets = {
            "last_dialysis_date": DatePickerInput(format="%d/%m/%Y"),
            "dod": DatePickerInput(format="%d/%m/%Y"),
        }
