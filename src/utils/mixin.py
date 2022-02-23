from datetime import date
import re
from django import forms
from django.forms import ModelForm

NIC_ID_PATTERN = re.compile("^[a-z][0-9]{12}[a-z0-9]$", re.I)
PASS_ID_PATTERN = re.compile("^[a-z0-9]{13}$", re.I)

# Validation
class PatientFormValidationMixin(ModelForm):
    def clean(self):
        errors = []
        current_date = date.today()
        cleaned_data = super().clean()
        id_type = cleaned_data.get("id_type")
        patient_id = cleaned_data.get("pid")
        dob = cleaned_data.get("dob")

        if id_type is not None:
            if id_type == 1 and patient_id is not None:
                if not NIC_ID_PATTERN.match(patient_id):
                    errors.append(
                        "N.I.C. must be 14 characters and match expected pattern: 1letter12digits1alphanumeric."
                    )
            if id_type == 2 and patient_id is not None:
                if not PASS_ID_PATTERN.match(patient_id):
                    errors.append(
                        "Passport Id must be 13 characters and match expected pattern: 13alphanumerics."
                    )

        if dob is not None:
            if dob > current_date:
                errors.append(
                    f"Date of birth({dob.strftime('%d/%m/%Y')}) cannot be after current date({current_date.strftime('%d/%m/%Y')})."
                )

        if any(errors):
            raise forms.ValidationError(errors)
        return cleaned_data


class PatientAddressFormValidationMixin(ModelForm):
    def clean(self):
        errors = []
        cleaned_data = super().clean()

        postcode = cleaned_data.get("postcode")

        if postcode is not None:
            if len(postcode) > 5:
                errors.append("Postcode is not valid.")

        if any(errors):
            raise forms.ValidationError(errors)
        return cleaned_data


class PatientMeasurementFormValidationMixin(ModelForm):
    def clean(self):
        errors = []
        cleaned_data = super().clean()

        measurementtype = cleaned_data.get("measurementtype")
        measurementvalue = cleaned_data.get("measurementvalue")

        if measurementtype is not None:
            if measurementtype == 1 and measurementvalue is not None:
                # Height, valid range 40 - 272 cm
                if (
                    measurementvalue < 40
                    or measurementvalue > 272
                    or round(measurementvalue, 2) != measurementvalue
                ):
                    errors.append("Height is not valid.")

            if measurementtype == 2 and measurementvalue is not None:
                # Weight, valid range 0.9 - 250 kg
                if (
                    measurementvalue < 0.9
                    or measurementvalue > 250
                    or round(measurementvalue, 2) != measurementvalue
                ):
                    errors.append("Weight is not valid.")

            if measurementtype == 3 and measurementvalue is not None:
                # Birth weight, valid range 0.9 to 9.9 kg
                if (
                    measurementvalue < 0.9
                    or measurementvalue > 9.9
                    or round(measurementvalue, 2) != measurementvalue
                ):
                    errors.append("Birth weight is not valid.")
        if any(errors):
            raise forms.ValidationError(errors)
        return cleaned_data


class PatientAKIMeasurementFormValidationMixin(ModelForm):
    def clean(self):
        errors = []
        current_date = date.today()
        cleaned_data = super().clean()

        creatinine = cleaned_data.get("creatinine")
        egfr = cleaned_data.get("egfr")
        measurement_date = cleaned_data.get("measurement_date")

        if creatinine is not None:
            if (
                creatinine < 60
                or creatinine > 1500
                or round(creatinine, 2) != creatinine
            ):
                errors.append("Creatinine is not valid.")

        if egfr is not None:
            if egfr < 1 or egfr > 150 or round(egfr, 2) != egfr:
                errors.append("eGFR is not valid.")

        if measurement_date is not None:
            if measurement_date > current_date:
                errors.append(
                    f"Date of (creatinine, eGFR) measurement({measurement_date.strftime('%d/%m/%Y')}) cannot be after current date({current_date.strftime('%d/%m/%Y')})."
                )

        if any(errors):
            raise forms.ValidationError(errors)
        return cleaned_data


class ValidationFormMixin(ModelForm):
    def clean(self):
        errors = []
        cleaned_data = super().clean()

        if any(errors):
            error_msg = ["Please correct the errors and try again."]
            error_msg.append(errors)
            raise forms.ValidationError(error_msg)
        return cleaned_data
