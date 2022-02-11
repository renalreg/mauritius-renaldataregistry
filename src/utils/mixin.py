from django import forms
from django.forms import ModelForm


# Validation
class ValidationFormMixin(ModelForm):
    def clean(self):
        errors = []
        cleaned_data = super().clean()

        id_type = cleaned_data.get("id_type")
        patient_id = cleaned_data.get("id")

        if id_type == 1:
            if patient_id is not None:
                if len(patient_id) < 14:
                    errors.append("N.I.C. Id must be 14 characters.")

        if any(errors):
            error_msg = ["Please correct the errors and try again."]
            error_msg.append(errors)
            raise forms.ValidationError(error_msg)
        return cleaned_data
