"""
This file contains the class-based views that take a web request and returns a web response.
"""
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DetailView
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from renaldataregistry.models import (
    PatientRegistration,
    Patient,
    PatientRenalDiagnosis,
    PatientAKImeasurement,
    PatientKRTModality,
    PatientAssessment,
    PatientLPAssessment,
    PatientMedicationAssessment,
    PatientStop,
    PatientDialysisAssessment,
)
from renaldataregistry.forms import (
    PatientRegistrationForm,
    PatientForm,
    PatientRenalDiagnosisForm,
    PatientAKIMeasurementForm,
    PatientAssessmentForm,
    PatientAssessmentLPForm,
    PatientAssessmentMedicationForm,
    PatientStopForm,
    PatientKRTModalityForm,
    PatientAssessmentDialysisForm,
)


# pylint: disable=too-many-statements, too-many-boolean-expressions, too-many-branches, too-many-lines


class PatientView(LoginRequiredMixin, DetailView):
    """
    View a single patient's registration form details, related to the models:
    renaldataregistry.Patient
    renaldataregistry.PatientRegistration
    renaldataregistry.PatientRenalDiagnosis
    renaldataregistry.PatientKRTModality
    renaldataregistry.PatientAKImeasurement
    renaldataregistry.PatientAssessment
    """

    model = Patient
    template_name = "patient_view.html"

    def get_context_data(self, **kwargs):
        """
        Add extra information related to: renaldataregistry.PatientKRTModality, renaldataregistry.PatientAssessment and renaldataregistry.PatientRenalDiagnosis
        """
        context = super().get_context_data(**kwargs)
        patient = self.object

        # KRT modalities entered in the patient's registration form
        patient_krtmodalities = PatientKRTModality.objects.filter(
            patient=patient,
            created_at=patient.created_at,
        ).order_by("start_date")[:6]

        if patient_krtmodalities:
            context["patient_krtmodalities"] = patient_krtmodalities

        # assessment
        patient_assessement = PatientAssessment.objects.filter(
            patient=patient, created_at=patient.created_at
        ).first()

        if patient_assessement:
            context["patient_assessement"] = patient_assessement

        # renal diagnosis
        patientrenaldiagnoses = PatientRenalDiagnosis.objects.filter(patient=patient)
        for _, patientrenaldiagnosis in enumerate(patientrenaldiagnoses):
            if patientrenaldiagnosis.is_primary_renaldiagnosis:
                context["patient_primaryrenaldiagnosis"] = patientrenaldiagnosis
            else:
                context["patient_secondaryrenaldiagnosis"] = patientrenaldiagnosis

        return context


class PatientRegistrationListView(LoginRequiredMixin, ListView):
    """
    List all registered patients, related to the model renaldataregistry.PatientRegistration.
    """

    paginate_by = 15
    model = PatientRegistration
    count = 0

    def get_queryset(self):
        """
        Overwrite the get_query_set to add search option.
        Search patient by N.I.C or passport number, name, surname, health institution or unit number.
        """
        try:
            search_word = self.request.GET.get(
                "search_keyword",
            )
        except KeyError:
            search_word = None

        if search_word:
            result_patients = PatientRegistration.objects.filter(
                Q(health_institution__name__icontains=search_word)
                | Q(patient__name__icontains=search_word)
                | Q(patient__surname__icontains=search_word)
                | Q(patient__pid__icontains=search_word)
                | Q(unit_no1__icontains=search_word)
                | Q(unit_no2__icontains=search_word)
                | Q(unit_no3__icontains=search_word)
            ).order_by("patient__name")
            self.count = result_patients.count()
            return result_patients

        all_patientregistrations = (
            PatientRegistration.objects.prefetch_related("patient")
            .all()
            .order_by("patient__name")
        )
        self.count = all_patientregistrations.count()
        return all_patientregistrations

    def get_context_data(self, **kwargs):
        """
        Add search word to the context information for presenting the results.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context["search_word"] = self.request.GET.get("search_keyword")
            if context["search_word"]:
                context["count"] = self.count
        return context


class PatientRegistrationView(LoginRequiredMixin, UpdateView):
    """
    Create and edit a patient registration's form.
    The collected data is the one included in the paper form for a patient's registration, related to the models:
    renaldataregistry.Patient
    renaldataregistry.PatientRegistration
    renaldataregistry.PatientRenalDiagnosis
    renaldataregistry.PatientKRTModality
    renaldataregistry.PatientAKImeasurement
    renaldataregistry.PatientAssessment
    """

    def __init__(self):
        """
        Include attributes required for get_krt_modalities function.
        """
        self.all_patient_krt_modalities = [None] * 6

    def get_krt_modalities(self, patient):
        """
        Get the patient's 6 oldest KRT modalities created in the registration form.
        """
        i = 4
        # Loading chronology of KRT modalities (the 6 oldest ones) and sorting them in the relevant order for the patient registration form
        patient_krtmodalities = PatientKRTModality.objects.filter(
            patient=patient, created_at=patient.created_at
        ).order_by("start_date")[:6]
        # Rearranging krt modalities to meet chronology in patient registration form
        for i, patientkrtmodality in enumerate(patient_krtmodalities):
            if patientkrtmodality.is_current:
                # setting current modality
                self.all_patient_krt_modalities[5] = patientkrtmodality
            else:
                # rest of the krt modalities
                self.all_patient_krt_modalities[i] = patientkrtmodality

    def get(self, request, *args, **kwargs):
        """
        Present page to create and edit patient's registration data.
        """
        context = {}
        template_name = "patient_register.html"
        title = "Patient registration form"
        patient_renaldiagnoses = [None] * 2

        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        if patient_id:
            # Edit patient
            patient = get_object_or_404(Patient, id=patient_id)
            context["patient"] = patient
            patient_form = PatientForm(instance=patient)
            patientregistration_form = PatientRegistrationForm(
                instance=patient.patientregistration
            )

            patientrenaldiagnoses = PatientRenalDiagnosis.objects.filter(
                patient=patient
            )

            for _, patientrenaldiagnosis in enumerate(patientrenaldiagnoses):
                if patientrenaldiagnosis.is_primary_renaldiagnosis:
                    patient_renaldiagnoses[0] = patientrenaldiagnosis
                else:
                    patient_renaldiagnoses[1] = patientrenaldiagnosis

            try:
                patientrenaldiagnosis_form = PatientRenalDiagnosisForm(
                    prefix="primary", instance=patient_renaldiagnoses[0]
                )
            except PatientRenalDiagnosis.DoesNotExist:
                patientrenaldiagnosis_form = PatientRenalDiagnosisForm(prefix="primary")

            try:
                patientsecondaryrenaldiagnosis_form = PatientRenalDiagnosisForm(
                    prefix="secondary", instance=patient_renaldiagnoses[1]
                )
            except PatientRenalDiagnosis.DoesNotExist:
                patientsecondaryrenaldiagnosis_form = PatientRenalDiagnosisForm(
                    prefix="secondary"
                )

            self.get_krt_modalities(patient)
            try:
                patientkrtmodality_first_form = PatientKRTModalityForm(
                    prefix="krt_first", instance=self.all_patient_krt_modalities[0]
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_first_form = PatientKRTModalityForm(
                    prefix="krt_first"
                )

            try:
                patientkrtmodality_2_form = PatientKRTModalityForm(
                    prefix="krt_2", instance=self.all_patient_krt_modalities[1]
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_2_form = PatientKRTModalityForm(prefix="krt_2")

            try:
                patientkrtmodality_3_form = PatientKRTModalityForm(
                    prefix="krt_3", instance=self.all_patient_krt_modalities[2]
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_3_form = PatientKRTModalityForm(prefix="krt_3")

            try:
                patientkrtmodality_4_form = PatientKRTModalityForm(
                    prefix="krt_4", instance=self.all_patient_krt_modalities[3]
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_4_form = PatientKRTModalityForm(prefix="krt_4")

            try:
                patientkrtmodality_5_form = PatientKRTModalityForm(
                    prefix="krt_5", instance=self.all_patient_krt_modalities[4]
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_5_form = PatientKRTModalityForm(prefix="krt_5")

            try:
                patientkrtmodality_present_form = PatientKRTModalityForm(
                    prefix="krt_present", instance=self.all_patient_krt_modalities[5]
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_present_form = PatientKRTModalityForm(
                    prefix="krt_present"
                )

            try:
                patientakimeasurement_form = PatientAKIMeasurementForm(
                    instance=patient.patientakimeasurement
                )
            except PatientAKImeasurement.DoesNotExist:
                patientakimeasurement_form = PatientAKIMeasurementForm()

            # Choosing only the one created in the registration form (if exists) since more assessments can be added in the Assessment form view
            patient_assessement = PatientAssessment.objects.filter(
                patient=patient, created_at=patient.created_at
            ).first()
            try:
                patientassessment_form = PatientAssessmentForm(
                    instance=patient_assessement
                )
            except PatientAssessment.DoesNotExist:
                patientassessment_form = PatientAssessmentForm()
        else:
            # Add new patient
            patientregistration_form = PatientRegistrationForm()
            patient_form = PatientForm()
            patientrenaldiagnosis_form = PatientRenalDiagnosisForm(prefix="primary")
            patientsecondaryrenaldiagnosis_form = PatientRenalDiagnosisForm(
                prefix="secondary"
            )
            patientkrtmodality_first_form = PatientKRTModalityForm(prefix="krt_first")
            patientkrtmodality_2_form = PatientKRTModalityForm(prefix="krt_2")
            patientkrtmodality_3_form = PatientKRTModalityForm(prefix="krt_3")
            patientkrtmodality_4_form = PatientKRTModalityForm(prefix="krt_4")
            patientkrtmodality_5_form = PatientKRTModalityForm(prefix="krt_5")
            patientkrtmodality_present_form = PatientKRTModalityForm(
                prefix="krt_present"
            )
            patientakimeasurement_form = PatientAKIMeasurementForm()
            patientassessment_form = PatientAssessmentForm()
        context = {
            "patientregistration_form": patientregistration_form,
            "patient_form": patient_form,
            "patientrenaldiagnosis_form": patientrenaldiagnosis_form,
            "patientsecondaryrenaldiagnosis_form": patientsecondaryrenaldiagnosis_form,
            "patientkrtmodality_first_form": patientkrtmodality_first_form,
            "patientkrtmodality_2_form": patientkrtmodality_2_form,
            "patientkrtmodality_3_form": patientkrtmodality_3_form,
            "patientkrtmodality_4_form": patientkrtmodality_4_form,
            "patientkrtmodality_5_form": patientkrtmodality_5_form,
            "patientkrtmodality_present_form": patientkrtmodality_present_form,
            "patientakimeasurement_form": patientakimeasurement_form,
            "patientassessment_form": patientassessment_form,
            "view_title": title,
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handle data validation and persistence for the creation and edition of the patient's registration form.
        """
        aki_saved = ""
        patient_renaldiagnoses = [None] * 2

        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None
        if patient_id:
            # update existing patient
            patient = get_object_or_404(Patient, id=patient_id)

            patientregistration_form = PatientRegistrationForm(
                request.POST, instance=patient.patientregistration
            )
            patient_form = PatientForm(request.POST, instance=patient)

            patientrenaldiagnoses = PatientRenalDiagnosis.objects.filter(
                patient=patient
            )
            for _, patientrenaldiagnosis in enumerate(patientrenaldiagnoses):
                if patientrenaldiagnosis.is_primary_renaldiagnosis:
                    patient_renaldiagnoses[0] = patientrenaldiagnosis
                else:
                    patient_renaldiagnoses[1] = patientrenaldiagnosis

            try:
                patientrenaldiagnosis_form = PatientRenalDiagnosisForm(
                    request.POST,
                    prefix="primary",
                    instance=patient_renaldiagnoses[0],
                )
            except PatientRenalDiagnosis.DoesNotExist:
                patientrenaldiagnosis_form = PatientRenalDiagnosisForm(
                    request.POST, prefix="primary"
                )

            try:
                patientsecondaryrenaldiagnosis_form = PatientRenalDiagnosisForm(
                    request.POST,
                    prefix="secondary",
                    instance=patient_renaldiagnoses[1],
                )
            except PatientRenalDiagnosis.DoesNotExist:
                patientsecondaryrenaldiagnosis_form = PatientRenalDiagnosisForm(
                    request.POST, prefix="secondary"
                )

            # Chronology of KRT modalities (the 6 oldest ones)
            # Note. formset didnt order, thus, use multiple forms of PatientKRTModalityForm
            self.get_krt_modalities(patient)

            try:
                patientkrtmodality_first_form = PatientKRTModalityForm(
                    request.POST,
                    prefix="krt_first",
                    instance=self.all_patient_krt_modalities[0],
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_first_form = PatientKRTModalityForm(
                    request.POST, prefix="krt_first"
                )
            try:
                patientkrtmodality_2_form = PatientKRTModalityForm(
                    request.POST,
                    prefix="krt_2",
                    instance=self.all_patient_krt_modalities[1],
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_2_form = PatientKRTModalityForm(
                    request.POST, prefix="krt_2"
                )
            try:
                patientkrtmodality_3_form = PatientKRTModalityForm(
                    request.POST,
                    prefix="krt_3",
                    instance=self.all_patient_krt_modalities[2],
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_3_form = PatientKRTModalityForm(
                    request.POST, prefix="krt_3"
                )
            try:
                patientkrtmodality_4_form = PatientKRTModalityForm(
                    request.POST,
                    prefix="krt_4",
                    instance=self.all_patient_krt_modalities[3],
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_4_form = PatientKRTModalityForm(
                    request.POST, prefix="krt_4"
                )
            try:
                patientkrtmodality_5_form = PatientKRTModalityForm(
                    request.POST,
                    prefix="krt_5",
                    instance=self.all_patient_krt_modalities[4],
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_5_form = PatientKRTModalityForm(
                    request.POST, prefix="krt_5"
                )
            try:
                patientkrtmodality_present_form = PatientKRTModalityForm(
                    request.POST,
                    prefix="krt_present",
                    instance=self.all_patient_krt_modalities[5],
                )
            except PatientKRTModality.DoesNotExist:
                patientkrtmodality_present_form = PatientKRTModalityForm(
                    request.POST, prefix="krt_present"
                )

            try:
                patientakimeasurement_form = PatientAKIMeasurementForm(
                    request.POST, instance=patient.patientakimeasurement
                )
            except PatientAKImeasurement.DoesNotExist:
                patientakimeasurement_form = PatientAKIMeasurementForm(request.POST)

            # Choosing only the one created in the registration form (if exists) since more assessments can be added in the Assessment form view
            patient_assessement = PatientAssessment.objects.filter(
                patient=patient, created_at=patient.created_at
            ).first()

            try:
                patientassessment_form = PatientAssessmentForm(
                    request.POST, instance=patient_assessement
                )
            except PatientAssessment.DoesNotExist:
                patientassessment_form = PatientAssessmentForm(request.POST)
        else:
            # create new patient
            patientregistration_form = PatientRegistrationForm(request.POST)
            patient_form = PatientForm(request.POST)

            patientrenaldiagnosis_form = PatientRenalDiagnosisForm(
                request.POST, prefix="primary"
            )
            patientsecondaryrenaldiagnosis_form = PatientRenalDiagnosisForm(
                request.POST, prefix="secondary"
            )

            # 6 KRT modalities in registration form
            patientkrtmodality_first_form = PatientKRTModalityForm(
                request.POST, prefix="krt_first"
            )
            patientkrtmodality_2_form = PatientKRTModalityForm(
                request.POST, prefix="krt_2"
            )
            patientkrtmodality_3_form = PatientKRTModalityForm(
                request.POST, prefix="krt_3"
            )
            patientkrtmodality_4_form = PatientKRTModalityForm(
                request.POST, prefix="krt_4"
            )
            patientkrtmodality_5_form = PatientKRTModalityForm(
                request.POST, prefix="krt_5"
            )
            patientkrtmodality_present_form = PatientKRTModalityForm(
                request.POST, prefix="krt_present"
            )

            patientakimeasurement_form = PatientAKIMeasurementForm(request.POST)
            patientassessment_form = PatientAssessmentForm(request.POST)

        if (
            patient_form.is_valid()
            and patientregistration_form.is_valid()
            and patientrenaldiagnosis_form.is_valid()
            and patientsecondaryrenaldiagnosis_form.is_valid()
            and patientakimeasurement_form.is_valid()
            and patientkrtmodality_first_form.is_valid()
            and patientkrtmodality_2_form.is_valid()
            and patientkrtmodality_3_form.is_valid()
            and patientkrtmodality_4_form.is_valid()
            and patientkrtmodality_5_form.is_valid()
            and patientkrtmodality_present_form.is_valid()
            and patientassessment_form.is_valid()
        ):
            patient = patient_form.save()

            patientregistration = patientregistration_form.save(commit=False)
            patientregistration.patient = patient
            patientregistration.created_at = patient.created_at
            patientregistration.save()
            patientregistration_form.save_m2m()

            if patientrenaldiagnosis_form.has_changed():
                patientrenaldiagnosis = patientrenaldiagnosis_form.save(commit=False)
                patientrenaldiagnosis.patient = patient
                patientrenaldiagnosis.is_primary_renaldiagnosis = True
                patientrenaldiagnosis.save()

            if patientsecondaryrenaldiagnosis_form.has_changed():
                patientsecondaryrenaldiagnosis = (
                    patientsecondaryrenaldiagnosis_form.save(commit=False)
                )
                patientsecondaryrenaldiagnosis.patient = patient
                patientsecondaryrenaldiagnosis.save()

            # Registering the first KRT modality
            if any(
                item in patientkrtmodality_first_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_first = patientkrtmodality_first_form.save(
                    commit=False
                )
                patientkrtmodality_first.patient = patient
                patientkrtmodality_first.created_at = patient.created_at
                if self.all_patient_krt_modalities[0]:
                    patientkrtmodality_first.save(
                        update_fields=["modality", "start_date"]
                    )
                else:
                    patientkrtmodality_first.save()

            # Registering the rest of the KRT modalities
            if any(
                item in patientkrtmodality_2_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_2 = patientkrtmodality_2_form.save(commit=False)
                patientkrtmodality_2.patient = patient
                patientkrtmodality_2.created_at = patient.created_at
                if self.all_patient_krt_modalities[1]:
                    patientkrtmodality_2.save(update_fields=["modality", "start_date"])
                else:
                    patientkrtmodality_2.save()

            if any(
                item in patientkrtmodality_3_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_3 = patientkrtmodality_3_form.save(commit=False)
                patientkrtmodality_3.patient = patient
                patientkrtmodality_3.created_at = patient.created_at
                if self.all_patient_krt_modalities[2]:
                    patientkrtmodality_3.save(update_fields=["modality", "start_date"])
                else:
                    patientkrtmodality_3.save()

            if any(
                item in patientkrtmodality_4_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_4 = patientkrtmodality_4_form.save(commit=False)
                patientkrtmodality_4.patient = patient
                patientkrtmodality_4.created_at = patient.created_at
                if self.all_patient_krt_modalities[3]:
                    patientkrtmodality_4.save(update_fields=["modality", "start_date"])
                else:
                    patientkrtmodality_4.save()

            if any(
                item in patientkrtmodality_5_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_5 = patientkrtmodality_5_form.save(commit=False)
                patientkrtmodality_5.patient = patient
                patientkrtmodality_5.created_at = patient.created_at
                if self.all_patient_krt_modalities[4]:
                    patientkrtmodality_5.save(update_fields=["modality", "start_date"])
                else:
                    patientkrtmodality_5.save()

            # Registering the current KRT modality
            if any(
                item in patientkrtmodality_present_form.changed_data
                for item in ["modality", "start_date", "hd_unit"]
            ):
                # if there is any current krt modality, set this to false since the new one is the current one now
                patient_current_krtmodality = PatientKRTModality.objects.filter(
                    patient=patient, is_current=True
                ).first()
                if patient_current_krtmodality:
                    patient_current_krtmodality.is_current = False
                    patient_current_krtmodality.save(update_fields=["is_current"])
                # new current krt modality
                patientkrtmodality_present = patientkrtmodality_present_form.save(
                    commit=False
                )
                patientkrtmodality_present.is_current = True
                patientkrtmodality_present.patient = patient
                patientkrtmodality_present.created_at = patient.created_at
                if self.all_patient_krt_modalities[5]:
                    patientkrtmodality_present.save(
                        update_fields=["modality", "start_date", "hd_unit"]
                    )
                else:
                    patientkrtmodality_present.save()

            if patient.in_krt_modality == "Y":
                aki_saved = " AKI measures are null because patient is in KRT."
            else:
                if patientakimeasurement_form.has_changed():
                    patientakimeasures = patientakimeasurement_form.save(commit=False)
                    patientakimeasures.patient = patient
                    patientakimeasures.created_at = patient.created_at
                    patientakimeasures.save()

            if patientassessment_form.has_changed():
                patientassessment = patientassessment_form.save(commit=False)
                patientassessment.patient = patient
                patientassessment.created_at = patient.created_at
                patientassessment.save()
                # saving comorbidities and disabilities
                patientassessment_form.save_m2m()

            messages.success(
                self.request,
                "Completed." + aki_saved,
                extra_tags="alert",
            )
            return redirect("renaldataregistry:PatientRegistrationListView")
        messages.error(
            self.request,
            "The action was not completed, please see below.",
            extra_tags="alert",
        )
        context = {
            "patientregistration_form": patientregistration_form,
            "patient_form": patient_form,
            "patientrenaldiagnosis_form": patientrenaldiagnosis_form,
            "patientsecondaryrenaldiagnosis_form": patientsecondaryrenaldiagnosis_form,
            "patientkrtmodality_first_form": patientkrtmodality_first_form,
            "patientkrtmodality_2_form": patientkrtmodality_2_form,
            "patientkrtmodality_3_form": patientkrtmodality_3_form,
            "patientkrtmodality_4_form": patientkrtmodality_4_form,
            "patientkrtmodality_5_form": patientkrtmodality_5_form,
            "patientkrtmodality_present_form": patientkrtmodality_present_form,
            "patientakimeasurement_form": patientakimeasurement_form,
            "patientassessment_form": patientassessment_form,
        }
        return render(request, "patient_register.html", context)


class PatientModalityListView(LoginRequiredMixin, ListView):
    """
    List all patient's modalities, related to the model renaldataregistry.PatientKRTModality.
    """

    model = PatientKRTModality
    template_name = "patientmodality_list.html"

    def get_queryset(self):
        """
        Overwrite the get_query_set function to get patient's modalities order by start date.
        """
        try:
            patient_id = self.kwargs["patient_id"]
        except KeyError:
            patient_id = None

        all_patientkrtmodalities = PatientKRTModality.objects.filter(
            patient=patient_id
        ).order_by("start_date")

        return all_patientkrtmodalities


class PatientModalityDetailView(LoginRequiredMixin, DetailView):
    """
    View a patient's modality form details, related to the models:
    renaldataregistry.PatientKRTModality
    renaldataregistry.PatientAKImeasurement
    renaldataregistry.PatientAssessment
    """

    def get(self, request, *args, **kwargs):
        """
        Get modality data linked to the patient.
        """
        is_first_modality = "No"
        try:
            modality_id = kwargs["modality_id"]
        except KeyError:
            modality_id = None

        patientmodality = get_object_or_404(PatientKRTModality, pk=modality_id)
        patient = patientmodality.patient
        patientakimeasurement = PatientAKImeasurement.objects.filter(
            patient=patient, created_at=patientmodality.created_at
        ).first()
        patient_assessement = PatientAssessment.objects.filter(
            patient=patient, created_at=patientmodality.created_at
        ).first()
        previouspatientmodality = (
            PatientKRTModality.objects.filter(
                patient=patient, start_date__lt=patientmodality.start_date
            )
            .order_by("-start_date")[:1]
            .first()
        )
        # checking if this is the first KRT modality
        patient_first_krtmodality = (
            PatientKRTModality.objects.filter(patient=patient)
            .order_by("start_date")[:1]
            .first()
        )
        if patientmodality == patient_first_krtmodality:
            is_first_modality = "Yes"

        return render(
            request,
            "patientmodality_view.html",
            context={
                "patientmodality": patientmodality,
                "patientakimeasurement": patientakimeasurement,
                "patient_assessement": patient_assessement,
                "previouspatientmodality": previouspatientmodality,
                "is_first_modality": is_first_modality,
            },
        )


class PatientModalityView(LoginRequiredMixin, UpdateView):
    """
    Create and edit a patient's KRT modality form.
    The collected data is the one included in the paper form to start or change a KRT modality, related to the models:
    renaldataregistry.Patient
    renaldataregistry.PatientKRTModality
    renaldataregistry.PatientAKImeasurement
    renaldataregistry.PatientAssessment
    """

    def get(self, request, *args, **kwargs):
        """
        Present page to create and edit patient's KRT modality data.
        """
        template_name = "patient_modality.html"
        title = "Patient KRT modality form"
        krt_is_first = False

        try:
            modality_id = kwargs["modality_id"]
        except KeyError:
            modality_id = None

        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        if patient_id:
            # Start/Change of current modality
            patient = get_object_or_404(Patient, id=patient_id)
            patientkrtmodality_form = PatientKRTModalityForm()
            patientakimeasurement_form = PatientAKIMeasurementForm()
            patientassessment_form = PatientAssessmentForm()

            num_patientkrtmodalities = PatientKRTModality.objects.filter(
                patient=patient.id
            ).count()
            if not num_patientkrtmodalities:
                krt_is_first = True
        else:
            if modality_id:
                # Edition of modality
                modality = get_object_or_404(PatientKRTModality, id=modality_id)
                patient = modality.patient

                # patient's first KRT modality
                patient_first_krtmodality = (
                    PatientKRTModality.objects.filter(patient=patient)
                    .order_by("start_date")[:1]
                    .first()
                )
                if modality == patient_first_krtmodality:
                    krt_is_first = True

                patientkrtmodality_form = PatientKRTModalityForm(instance=modality)

                # There is only one record for creatinine, eGFR and Hb associated to the patient
                try:
                    patientakimeasurement_form = PatientAKIMeasurementForm(
                        instance=patient.patientakimeasurement
                    )
                except PatientAKImeasurement.DoesNotExist:
                    patientakimeasurement_form = PatientAKIMeasurementForm()

                # The patient assessment linked to the KRT modality form
                patient_assessement = PatientAssessment.objects.filter(
                    patient=patient, created_at=modality.created_at
                ).first()
                try:
                    patientassessment_form = PatientAssessmentForm(
                        instance=patient_assessement
                    )
                except PatientAssessment.DoesNotExist:
                    patientassessment_form = PatientAssessmentForm()
        context = {
            "patientkrtmodality_form": patientkrtmodality_form,
            "patientakimeasurement_form": patientakimeasurement_form,
            "patientassessment_form": patientassessment_form,
            "view_title": title,
            "krt_is_first": krt_is_first,
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handle data validation and persistence for the creation and edition of the patient's KRT modality form.
        """
        first_aki = False
        first_assess_for_krt = False

        try:
            modality_id = kwargs["modality_id"]
        except KeyError:
            modality_id = None

        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)

            patientkrtmodality_form = PatientKRTModalityForm(request.POST)
            patientakimeasurement_form = PatientAKIMeasurementForm(request.POST)
            patientassessment_form = PatientAssessmentForm(request.POST)
        else:
            if modality_id:
                modality = get_object_or_404(PatientKRTModality, id=modality_id)
                mod_start_date = modality.start_date
                patient = modality.patient

                patientkrtmodality_form = PatientKRTModalityForm(
                    request.POST, instance=modality
                )

                try:
                    patientakimeasurement_form = PatientAKIMeasurementForm(
                        request.POST, instance=patient.patientakimeasurement
                    )
                except PatientAKImeasurement.DoesNotExist:
                    patientakimeasurement_form = PatientAKIMeasurementForm(request.POST)
                    first_aki = True

                # The patient assessment linked to the KRT modality form
                patient_assessement = PatientAssessment.objects.filter(
                    patient=patient, created_at=modality.created_at
                ).first()
                if not patient_assessement:
                    first_assess_for_krt = True
                try:
                    patientassessment_form = PatientAssessmentForm(
                        request.POST, instance=patient_assessement
                    )
                except PatientAssessment.DoesNotExist:
                    patientassessment_form = PatientAssessmentForm(request.POST)
        if (
            patientkrtmodality_form.is_valid()
            and patientakimeasurement_form.is_valid()
            and patientassessment_form.is_valid()
        ):
            if patient_id:
                # Creation of new current KRT modality
                # Existing current KRT modality becomes part of the chronology
                # Note. This means that the registration form included a current krt modality
                patient_current_krtmodality = PatientKRTModality.objects.filter(
                    patient=patient, is_current=True
                ).first()
                if patient_current_krtmodality:
                    patient_current_krtmodality.is_current = False
                    patient_current_krtmodality.save()
                else:
                    # The first current krt modality of the patient is inserted in the KRT modality form (and not in the registration form)
                    patient.in_krt_modality = "Y"
                    patient.save()

                # The KRT modality of the form becomes the current KRT modality of the patient
                creation_date = timezone.now()
                if patientkrtmodality_form.has_changed():
                    patientkrtmodality = patientkrtmodality_form.save(commit=False)
                    patientkrtmodality.patient = patient
                    patientkrtmodality.created_at = creation_date
                    patientkrtmodality.is_current = True
                    patientkrtmodality.start_date = creation_date.date()
                    patientkrtmodality.save()

                if patientakimeasurement_form.has_changed():
                    patientakimeasurement = patientakimeasurement_form.save(
                        commit=False
                    )
                    patientakimeasurement.patient = patient
                    patientakimeasurement.created_at = creation_date
                    patientakimeasurement.save()

                if patientassessment_form.has_changed():
                    patientassessment = patientassessment_form.save(commit=False)
                    patientassessment.patient = patient
                    patientassessment.created_at = creation_date
                    patientassessment.save()
                    patientassessment_form.save_m2m()
            else:
                # Edition of KRT modality
                if modality_id:
                    modality = patientkrtmodality_form.save(commit=False)
                    modality.start_date = mod_start_date
                    modality.save()

                    if patientakimeasurement_form.has_changed():
                        patientakimeasurement = patientakimeasurement_form.save(
                            commit=False
                        )
                        patientakimeasurement.patient = patient
                        if first_aki:
                            patientakimeasurement.created_at = modality.created_at
                        patientakimeasurement.save()

                    if patientassessment_form.has_changed():
                        patientassessment = patientassessment_form.save(commit=False)
                        patientassessment.patient = patient
                        if first_assess_for_krt:
                            patientassessment.created_at = modality.created_at
                        patientassessment.save()
                        patientassessment_form.save_m2m()

                    patient_id = modality.patient.id

            messages.success(
                self.request,
                "Completed.",
                extra_tags="alert",
            )
            return redirect(
                "renaldataregistry:PatientModalityListView", patient_id=patient_id
            )
        messages.error(
            self.request,
            "The action was not completed, please see below.",
            extra_tags="alert",
        )
        context = {
            "patientkrtmodality_form": patientkrtmodality_form,
            "patientakimeasurement_form": patientakimeasurement_form,
            "patientassessment_form": patientassessment_form,
            "krt_is_first": request.POST.get("krt_is_first"),
        }
        return render(request, "patient_modality.html", context)


class PatientAssessmentListView(LoginRequiredMixin, ListView):
    """
    List all patient's dialysis assessments, related to the models:
    renaldataregistry.PatientKRTModality
    renaldataregistry.PatientAssessment
    Assessments are dialysis assessments. The paper form corresponds to NRR B0.3 Assessment dialysis.pdf
    """

    model = PatientAssessment

    def get_context_data(self, **kwargs):
        """
        Add extra information to identify if patient is in dialysis mode.
        """
        patient_in_dialysis = False
        context = super().get_context_data(**kwargs)

        try:
            patient_id = self.kwargs["patient_id"]
        except KeyError:
            patient_id = None

        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)

            patient_current_krtmodality = PatientKRTModality.objects.filter(
                patient=patient, is_current=True
            ).first()

            # Showing only dialysis assessments in this view
            # created_at__gt=patient.created_at ignores the initial assessment created in the registration form (if exists)
            all_patientassessments = PatientAssessment.objects.filter(
                patient=patient_id, created_at__gt=patient.created_at
            ).order_by("created_at")

            if patient_current_krtmodality:
                # KRT modes 2, 3
                if patient_current_krtmodality.modality in (2, 3):
                    patient_in_dialysis = True

            context = {
                "patient_in_dialysis": patient_in_dialysis,
                "patient": patient,
                "patientassessment_list": all_patientassessments,
            }
        return context


class PatientAssessmentDetailView(LoginRequiredMixin, DetailView):
    """
    View a patient's dialysis assessment form details, related to the models:
    renaldataregistry.PatientKRTModality
    renaldataregistry.PatientAssessment
    """

    def get(self, request, *args, **kwargs):
        """
        Get dialysis assessment data linked to the patient.
        """
        current_krt_is_first_dialysis = False
        try:
            assessment_id = kwargs["assessment_id"]
        except KeyError:
            assessment_id = None

        patientassesment = get_object_or_404(PatientAssessment, pk=assessment_id)
        patient = patientassesment.patient

        patient_current_krtmodality = PatientKRTModality.objects.filter(
            patient=patient, is_current=True
        ).first()

        # patient's first KRT modality
        patient_first_krtmodality = (
            PatientKRTModality.objects.filter(patient=patient)
            .order_by("start_date")[:1]
            .first()
        )

        # HD, modality 2
        # PD, modality 3
        if (
            patient_first_krtmodality.modality in (2, 3)
            and patient_current_krtmodality == patient_first_krtmodality
        ):
            current_krt_is_first_dialysis = True

        return render(
            request,
            "patientassessment_view.html",
            context={
                "patientassesment": patientassesment,
                "patient_current_krtmodality": patient_current_krtmodality,
                "current_krt_is_first_dialysis": current_krt_is_first_dialysis,
            },
        )


class PatientAssessmentView(LoginRequiredMixin, UpdateView):
    """
    Create and edit a patient's dialysis assessment form.
    The collected data is the one included in the paper form to add assessment for dialysis patient, related to the models:
    renaldataregistry.Patient
    renaldataregistry.PatientKRTModality
    renaldataregistry.PatientLPAssessment
    renaldataregistry.PatientMedicationAssessment
    renaldataregistry.PatientDialysisAssessment
    """

    def get(self, request, *args, **kwargs):
        """
        Present page to create and edit patient's dialysis assessment data.
        """
        template_name = "patient_assess.html"
        title = "Patient assessment form"

        try:
            assessment_id = kwargs["assessment_id"]
        except KeyError:
            assessment_id = None

        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        if patient_id:
            # Create a new assessment for the patient
            patient = get_object_or_404(Patient, id=patient_id)

            # There are assessments parameters linked to the current KRT modality. They depend on HD or PD.
            # Example, Sessions/week or Mins/session for HD modality
            # Exchanges/day or Fluid litres/day for PD modality
            patient_current_krtmodality = PatientKRTModality.objects.filter(
                patient=patient, is_current=True
            ).first()
            patientkrtmodality_form = PatientKRTModalityForm(
                instance=patient_current_krtmodality
            )
            patientassessmentlp_form = PatientAssessmentLPForm()
            patientassessmentmed_form = PatientAssessmentMedicationForm()
            patientassessment_form = PatientAssessmentForm()
            patientassessmentdia_form = PatientAssessmentDialysisForm()
        else:
            if assessment_id:
                # Edition of patient's assessment
                assessment = get_object_or_404(PatientAssessment, id=assessment_id)
                patient = assessment.patient

                patientassessment_form = PatientAssessmentForm(instance=assessment)

                patient_current_krtmodality = PatientKRTModality.objects.filter(
                    patient=patient, is_current=True
                ).first()
                patientkrtmodality_form = PatientKRTModalityForm(
                    instance=patient_current_krtmodality
                )

                try:
                    patientassessmentlp_form = PatientAssessmentLPForm(
                        instance=assessment.patientlpassessment
                    )
                except PatientLPAssessment.DoesNotExist:
                    patientassessmentlp_form = PatientAssessmentLPForm()

                try:
                    patientassessmentmed_form = PatientAssessmentMedicationForm(
                        instance=assessment.patientmedicationassessment
                    )
                except PatientMedicationAssessment.DoesNotExist:
                    patientassessmentmed_form = PatientAssessmentMedicationForm()

                try:
                    patientassessmentdia_form = PatientAssessmentDialysisForm(
                        instance=assessment.patientdialysisassessment
                    )
                except PatientDialysisAssessment.DoesNotExist:
                    patientassessmentdia_form = PatientAssessmentDialysisForm()
        context = {
            "patientkrtmodality_form": patientkrtmodality_form,
            "patientassessmentlp_form": patientassessmentlp_form,
            "patientassessmentmed_form": patientassessmentmed_form,
            "patientassessment_form": patientassessment_form,
            "view_title": title,
            "patient_current_krtmodality": patient_current_krtmodality,
            "patientassessmentdia_form": patientassessmentdia_form,
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handle data validation and persistence for the creation and edition of the patient's dialysis assessment form.
        """
        try:
            assessment_id = kwargs["assessment_id"]
        except KeyError:
            assessment_id = None

        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        if patient_id:
            # Adding new assessment
            patient = get_object_or_404(Patient, id=patient_id)

            patient_current_krtmodality = PatientKRTModality.objects.filter(
                patient=patient, is_current=True
            ).first()

            # existing patient KRT modality (dialysis modality)
            patientkrtmodality_form = PatientKRTModalityForm(
                request.POST, instance=patient_current_krtmodality
            )
            patientassessmentlp_form = PatientAssessmentLPForm(request.POST)
            patientassessmentmed_form = PatientAssessmentMedicationForm(request.POST)
            patientassessment_form = PatientAssessmentForm(request.POST)
            patientassessmentdia_form = PatientAssessmentDialysisForm(request.POST)
        else:
            if assessment_id:
                # Edit existing assessment
                assessment = get_object_or_404(PatientAssessment, id=assessment_id)
                patient = assessment.patient

                patientassessment_form = PatientAssessmentForm(
                    request.POST, instance=assessment
                )

                patient_current_krtmodality = PatientKRTModality.objects.filter(
                    patient=patient, is_current=True
                ).first()
                patientkrtmodality_form = PatientKRTModalityForm(
                    request.POST, instance=patient_current_krtmodality
                )

                try:
                    patientassessmentlp_form = PatientAssessmentLPForm(
                        request.POST, instance=assessment.patientlpassessment
                    )
                except PatientLPAssessment.DoesNotExist:
                    patientassessmentlp_form = PatientAssessmentLPForm(request.POST)

                try:
                    patientassessmentmed_form = PatientAssessmentMedicationForm(
                        request.POST, instance=assessment.patientmedicationassessment
                    )
                except PatientMedicationAssessment.DoesNotExist:
                    patientassessmentmed_form = PatientAssessmentMedicationForm(
                        request.POST
                    )

                try:
                    patientassessmentdia_form = PatientAssessmentDialysisForm(
                        request.POST, instance=assessment.patientdialysisassessment
                    )
                except PatientDialysisAssessment.DoesNotExist:
                    patientassessmentdia_form = PatientAssessmentDialysisForm(
                        request.POST
                    )
        if (
            patientkrtmodality_form.is_valid()
            and patientassessmentlp_form.is_valid()
            and patientassessmentmed_form.is_valid()
            and patientassessment_form.is_valid()
            and patientassessmentdia_form.is_valid()
        ):
            if patient_id:
                # fot the creation of a new assessment
                creation_date = timezone.now()

            # The KRT modality already exists, update correspondant fields for HD modality
            # modality 2, HD
            if patient_current_krtmodality.modality == 2:
                patient_current_krtmodality.save(
                    update_fields=["hd_unit", "hd_initialaccess", "hd_tc_ntc_reason"]
                )

            patientassessment = patientassessment_form.save(commit=False)
            patientassessment.patient = patient
            if patient_id:
                # creating a new assessment
                patientassessment.created_at = creation_date
            patientassessment.save()
            patientassessment_form.save_m2m()

            if patientassessmentlp_form.has_changed():
                patientassessmentlp = patientassessmentlp_form.save(commit=False)
                patientassessmentlp.patientassessment = patientassessment
                patientassessmentlp.save()

            if patientassessmentmed_form.has_changed():
                patientassessmentmed = patientassessmentmed_form.save(commit=False)
                patientassessmentmed.patientassessment = patientassessment
                patientassessmentmed.save()

            if patientassessmentdia_form.has_changed():
                patientassessmentdia = patientassessmentdia_form.save(commit=False)
                patientassessmentdia.patientassessment = patientassessment
                patientassessmentdia.save()
            messages.success(
                self.request,
                "Completed.",
                extra_tags="alert",
            )

            if not patient_id:
                patient_id = patient.id
            return redirect(
                "renaldataregistry:PatientAssessmentListView", patient_id=patient_id
            )
        messages.error(
            self.request,
            "The action was not completed, please see below.",
            extra_tags="alert",
        )
        context = {
            "patientkrtmodality_form": patientkrtmodality_form,
            "patientassessmentlp_form": patientassessmentlp_form,
            "patientassessmentmed_form": patientassessmentmed_form,
            "patientassessment_form": patientassessment_form,
            "patient_current_krtmodality": patient_current_krtmodality,
            "patientassessmentdia_form": patientassessmentdia_form,
        }
        return render(request, "patient_assess.html", context)


class PatientStopView(LoginRequiredMixin, UpdateView):
    """
    Create and edit a patient's stopping dialysis form.
    The collected data is the one included in the paper form to add stopping dialysis data, related to the models:
    renaldataregistry.Patient
    renaldataregistry.PatientStop
    """

    def get(self, request, *args, **kwargs):
        """
        Present page to create and edit patient's stopping dialysis data.
        """
        title = "Patient stopping dialysis form"
        patient_current_krt_is_dialysis = False
        patientstop_form = PatientStopForm()

        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        patient = get_object_or_404(Patient, id=patient_id)

        try:
            patientstop_form = PatientStopForm(instance=patient.patientstop)
            patient_current_krt_is_dialysis = True
        except PatientStop.DoesNotExist:
            patient_current_krtmodality = PatientKRTModality.objects.filter(
                patient=patient, is_current=True
            ).first()
            # check if patient is in dialysis mode (HD or PD)
            if patient_current_krtmodality.modality in (2, 3):
                patient_current_krt_is_dialysis = True
                if not patient_current_krt_is_dialysis:
                    title = "Patient is not in dialysis"

        return render(
            request,
            "patient_stop.html",
            context={
                "patientstop_form": patientstop_form,
                "view_title": title,
                "patient_current_krt_is_dialysis": patient_current_krt_is_dialysis,
            },
        )

    def post(self, request, *args, **kwargs):
        """
        Handle data validation and persistence for the creation and edition of the patient's stopping dialysis form.
        When a patient stop dialysis, no more dialysis assessment's forms are allowed, unless that the patient registers a new KRT dialysis modality.
        """
        title = "Patient stopping dialysis form"
        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        patient = get_object_or_404(Patient, id=patient_id)

        try:
            patientstop_form = PatientStopForm(
                request.POST, instance=patient.patientstop
            )
        except PatientStop.DoesNotExist:
            patientstop_form = PatientStopForm(request.POST)

        if patientstop_form.is_valid():
            if patientstop_form.has_changed():
                patientstop = patientstop_form.save(commit=False)
                patientstop.patient = patient
                patientstop.save()

                patient_current_krtmodality = PatientKRTModality.objects.filter(
                    patient=patient, is_current=True
                ).first()
                if patient_current_krtmodality:
                    patient_current_krtmodality.is_current = False
                    patient_current_krtmodality.save(update_fields=["is_current"])

            messages.success(
                self.request,
                "Completed.",
                extra_tags="alert",
            )
            return redirect("renaldataregistry:PatientRegistrationListView")
        messages.error(
            self.request,
            "The action was not completed, please see below.",
            extra_tags="alert",
        )
        return render(
            request,
            "patient_stop.html",
            context={"patientstop_form": patientstop_form, "view_title": title},
        )


class PatientRegistrationHistoryView(LoginRequiredMixin, DetailView):
    """
    View a patient's registration history, related to the models:
    renaldataregistry.Patient
    renaldataregistry.PatientRegistration
    """

    def get(self, request, *args, **kwargs):
        """
        Present page to list history of health institutions were the patient has been registered.
        """
        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        patientregistration = get_object_or_404(PatientRegistration, pk=patient_id)

        return render(
            request,
            "patientregistration_history.html",
            context={"patientregistration": patientregistration},
        )
