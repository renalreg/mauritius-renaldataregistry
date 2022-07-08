"""
This file contains custom validation for the forms' fields.
"""
from datetime import date
import re
from django import forms
from django.forms import ModelForm

# pylint: disable=too-many-branches, too-many-statements

NIC_ID_PATTERN = re.compile("^[a-z][0-9]{12}[a-z0-9]$", re.I)
PASS_ID_PATTERN = re.compile("^[a-z0-9]{13}$", re.I)
EMAIL_PATTERN = re.compile(r"[^@]+@[^@]+\.[^@]+", re.I)
POSTCODE_PATTERN = re.compile("^[0-9]{5}$", re.I)

# Validation
class PatientFormValidationMixin(ModelForm):
    def clean(self):
        errors = []
        current_date = date.today()
        cleaned_data = super().clean()
        id_type = cleaned_data.get("id_type")
        patient_id = cleaned_data.get("pid")
        dob = cleaned_data.get("dob")
        height = cleaned_data.get("height")
        weight = cleaned_data.get("weight")
        birth_weight = cleaned_data.get("birth_weight")
        postcode = cleaned_data.get("postcode")
        landline_number = cleaned_data.get("landline_number")
        mobile_number = cleaned_data.get("mobile_number")
        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")

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
                    f"Date of birth({dob.strftime('%d/%m/%Y')}) cannot be after current date ({current_date.strftime('%d/%m/%Y')})."
                )
        if height is not None:
            # Height, valid range 40 - 272 cm
            if height < 40 or height > 272:  # or round(height, 2) != height:
                errors.append("Height valid range is 40 - 272 cm.")

        if weight is not None:
            # Weight, valid range 0.9 - 250 kg
            if weight < 0.86 or weight > 250:  # or round(weight, 2) != weight:
                errors.append("Weight valid range is 0.9 - 250 kg.")

        if birth_weight is not None:
            if (
                birth_weight < 0.86
                or birth_weight > 9.9
                or round(birth_weight, 2) != birth_weight
            ):
                errors.append("Birth weight valid range is 0.9 - 9.9 kg.")

        if postcode is not None:
            if not POSTCODE_PATTERN.match(postcode):
                errors.append("Postcode must be 5 digits.")

        if landline_number is not None:
            # Landline, 7 digits. No area codes.
            if len(landline_number) != 7 or not landline_number.isnumeric():
                errors.append("Landline number is 7 digits.")

        if mobile_number is not None:
            # Mobile, 8 digits. No area codes.
            if len(mobile_number) != 8 or not mobile_number.isnumeric():
                errors.append("Mobile number is 8 digits.")

        if email is not None:
            # Email
            if not EMAIL_PATTERN.match(email):
                errors.append("Email must contain @ and at least one . symbol.")

        if email2 is not None:
            # Email
            if not EMAIL_PATTERN.match(email2):
                errors.append("Email must contain @ and at least one . symbol.")

        if any(errors):
            raise forms.ValidationError(errors)
        return cleaned_data


class PatientRegistrationFormValidationMixin(ModelForm):
    def clean(self):
        errors = []
        cleaned_data = super().clean()

        health_institution = cleaned_data.get("health_institution")
        is_unit_required = health_institution.is_unit_required
        unit_no1 = cleaned_data.get("unit_no1")
        unit_no2 = cleaned_data.get("unit_no2")
        unit_no3 = cleaned_data.get("unit_no3")

        if is_unit_required and not (unit_no1 or unit_no2 or unit_no3):
            errors.append(
                "Unit number for the selected health institution is required."
            )

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
                errors.append("Creatinine valid range is 60 - 1500 \u03BCmol/l.")
        if egfr is not None:
            if egfr < 1 or egfr > 150 or round(egfr, 2) != egfr:
                errors.append("eGFR valid range is 1 to 150 ml/min/1.73m2.")
        if measurement_date is not None:
            if measurement_date > current_date:
                errors.append(
                    f"Date of (creatinine, eGFR) measurement({measurement_date.strftime('%d/%m/%Y')}) cannot be after current date ({current_date.strftime('%d/%m/%Y')})."
                )
        if any(errors):
            raise forms.ValidationError(errors)
        return cleaned_data


class PatientKRTModalityFormValidationMixin(ModelForm):
    def clean(self):
        errors = []
        current_date = date.today()
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")

        if start_date is not None:
            if start_date > current_date:
                errors.append(
                    f"The KRT start date ({start_date.strftime('%d/%m/%Y')}) cannot be after current date ({current_date.strftime('%d/%m/%Y')})."
                )
        if any(errors):
            raise forms.ValidationError(errors)
        return cleaned_data
