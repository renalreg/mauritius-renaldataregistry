from django import forms
from crispy_forms.bootstrap import TabHolder, Tab, StrictButton
from crispy_forms.helper import FormHelper
from bootstrap_datepicker_plus import DatePickerInput
from .models import (
    PatientRegistration,
    Patient,
    PatientAddress,
    PatientContact,
    PatientMeasurement,
    PatientOccupation,
    PatientKRTModality,
    PatientAKImeasurement,
    PatientAssessment,
    LaboratoryParameter,
    Medication,
)
from utils.mixin import ValidationFormMixin
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from django.forms import BaseInlineFormSet
import pdb



class CustomInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CustomInlineFormSet, self).__init__(*args, **kwargs)
        # no_of_forms = len(self)
        self[0].fields['contactvalue'].label = "Phone No." # phone
        self[1].fields['contactvalue'].label = "Mobile phone No." # mobile
        self[2].fields['contactvalue'].label = "Other phone No." # alt_phone1
        self[3].fields['contactvalue'].label = "Other phone No." # alt_phone2
        self[4].fields['contactvalue'].label = "Email" # email
        self[5].fields['contactvalue'].label = "Alternative email" # alt_email
        # for i in range(0, no_of_forms):
        #     self[i].fields['contactvalue'].label += "-%d" % (i + 1)


class PatientRegistrationForm(ValidationFormMixin):
    class Meta:
        model = PatientRegistration
        fields = ["health_institution", "unit"]


class PatientForm(ValidationFormMixin):
    class Meta:
        model = Patient
        exclude = ["created_by", "updated_by"]
        widgets = {
            "dob": DatePickerInput(format="%d/%m/%Y"),
        }


class PatientAddressForm(ValidationFormMixin):
    class Meta:
        model = PatientAddress
        fields = ["street", "postcode"]


class PatientContactForm(ValidationFormMixin):
    class Meta:
        model = PatientContact
        fields = ["contactvalue"]
        # labels = {"contactvalue": "Contact"}

PatientContactFormSet = inlineformset_factory(Patient, PatientContact,
                                            form=PatientContactForm, formset=CustomInlineFormSet, extra=6)

class PatientMeasurementForm(ValidationFormMixin):
    class Meta:
        model = PatientMeasurement
        fields = ["measurementvalue"]
        labels = {"measurementvalue": ""}


class PatientOccupationForm(ValidationFormMixin):
    class Meta:
        model = PatientOccupation
        fields = ["occupation"]
        labels = {"occupation": ""}


class PatientKRTModalityForm(ValidationFormMixin):
    class Meta:
        model = PatientKRTModality
        exclude = ["created_by", "updated_by"]
        widgets = {
            "start_date": DatePickerInput(format="%d/%m/%Y"),
        }


class PatientAKIMeasurement(ValidationFormMixin):
    class Meta:
        model = PatientAKImeasurement
        fields = ["creatinine", "egfr", "measurement_date"]


class PatientAssessmentForm(ValidationFormMixin):
    class Meta:
        model = PatientAssessment
        exclude = ["created_by", "updated_by"]


class PatientAssessmentLPForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_lp = LaboratoryParameter.objects.all()

        for i in range(len(all_lp)):
            field_name = all_lp[i].parameter
            self.fields[field_name] = forms.DecimalField(
                decimal_places=2, max_digits=5, required=False
            )


class PatientAssessmentMedicationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_med = Medication.objects.all()

        ANS_CHOICES = (
            (1, "Yes"),
            (2, "No"),
        )

        for i in range(len(all_med)):
            field_name = all_med[i].medication

            if all_med[i].type == 3 or all_med[i].type == 4:
                self.fields[field_name] = forms.ChoiceField(choices=ANS_CHOICES)
            else:
                self.fields[field_name] = forms.DecimalField(
                    decimal_places=2, max_digits=5, required=False
                )
