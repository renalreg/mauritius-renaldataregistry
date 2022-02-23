from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from bootstrap_datepicker_plus.widgets import DatePickerInput  # type: ignore
from utils.mixin import (
    ValidationFormMixin,
    PatientFormValidationMixin,
    PatientAddressFormValidationMixin,
    PatientMeasurementFormValidationMixin,
    PatientAKIMeasurementFormValidationMixin,
)
from .models import (
    PatientRegistration,
    Patient,
    PatientAddress,
    PatientContact,
    PatientMeasurement,
    PatientOccupation,
    PatientRenalDiagnosis,
    PatientKRTModality,
    PatientAKImeasurement,
    PatientAssessment,
    LaboratoryParameter,
    Medication,
    PatientStop,
)


class CustomInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # no_of_forms = len(self)
        self[0].fields["contactvalue"].label = "Phone No."  # phone
        self[1].fields["contactvalue"].label = "Mobile phone No."  # mobile
        self[2].fields["contactvalue"].label = "Other phone No."  # alt_phone1
        self[3].fields["contactvalue"].label = "Other phone No."  # alt_phone2
        self[4].fields["contactvalue"].label = "Email"  # email
        self[5].fields["contactvalue"].label = "Alternative email"  # alt_email
        # for i in range(0, no_of_forms):
        #     self[i].fields['contactvalue'].label += "-%d" % (i + 1)


class CustomMeasurementInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self[0].fields["measurementvalue"].label = "Height (cm)"
        self[1].fields["measurementvalue"].label = "Weight (kg)"
        self[2].fields["measurementvalue"].label = "Birth weight (kg)"


class CustomOccupationInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self[0].fields["occupation"].label = "Current employment"
        self[1].fields["occupation"].label = "Significant previous occupation 1"
        self[2].fields["occupation"].label = "Significant previous occupation 2"
        self[3].fields["occupation"].label = "Significant previous occupation 3"
        self[4].fields["occupation"].label = "Significant previous occupation 4"


class PatientRegistrationForm(ValidationFormMixin):
    class Meta:
        model = PatientRegistration
        fields = ["health_institution", "unit"]


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
        ]
        widgets = {
            "dob": DatePickerInput(format="%d/%m/%Y"),
        }


class PatientAddressForm(PatientAddressFormValidationMixin):
    class Meta:
        model = PatientAddress
        fields = ["street", "postcode"]


class PatientContactForm(ValidationFormMixin):
    class Meta:
        model = PatientContact
        fields = ["contactvalue"]


PatientContactFormSet = inlineformset_factory(
    Patient,
    PatientContact,
    form=PatientContactForm,
    formset=CustomInlineFormSet,
    extra=6,
)


class PatientMeasurementForm(PatientMeasurementFormValidationMixin):
    class Meta:
        model = PatientMeasurement
        fields = ["measurementvalue", "measurementtype"]


PatientMeasurementFormSet = inlineformset_factory(
    Patient,
    PatientMeasurement,
    form=PatientMeasurementForm,
    formset=CustomMeasurementInlineFormSet,
    extra=3,
    can_delete=False,
)


class PatientOccupationForm(ValidationFormMixin):
    class Meta:
        model = PatientOccupation
        fields = ["occupation"]


PatientOccupationFormSet = inlineformset_factory(
    Patient,
    PatientOccupation,
    form=PatientOccupationForm,
    formset=CustomOccupationInlineFormSet,
    extra=5,
)


class PatientRenalDiagnosisForm(ValidationFormMixin):
    class Meta:
        model = PatientRenalDiagnosis
        fields = ["renaldiagnosis"]


class PatientKRTModalityForm(ValidationFormMixin):
    class Meta:
        model = PatientKRTModality
        fields = [
            "modality",
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


PatientKRTModalityFormSet = inlineformset_factory(
    Patient,
    PatientKRTModality,
    form=PatientKRTModalityForm,
    extra=6,
)


class PatientAKIMeasurementForm(PatientAKIMeasurementFormValidationMixin):
    class Meta:
        model = PatientAKImeasurement
        fields = ["creatinine", "egfr", "hb", "measurement_date"]
        widgets = {
            "measurement_date": DatePickerInput(format="%d/%m/%Y"),
        }


class PatientAssessmentForm(ValidationFormMixin):
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


class PatientAssessmentLPForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_lp = LaboratoryParameter.objects.all()

        for _, laboratory_parameter in enumerate(all_lp):
            field_name = laboratory_parameter.parameter
            self.fields[field_name] = forms.DecimalField(
                decimal_places=2, max_digits=5, required=False
            )


class PatientAssessmentMedicationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_med = Medication.objects.all()

        answer_choices = (
            (1, "Yes"),
            (2, "No"),
        )

        for _, medication in enumerate(all_med):
            field_name = medication.medication

            if medication.type in (3, 4):
                self.fields[field_name] = forms.ChoiceField(choices=answer_choices)
            else:
                self.fields[field_name] = forms.DecimalField(
                    decimal_places=2, max_digits=5, required=False
                )


class PatientStopForm(ValidationFormMixin):
    class Meta:
        model = PatientStop
        fields = ["last_dialysis_date", "stop_reason", "dod", "cause_of_death"]
