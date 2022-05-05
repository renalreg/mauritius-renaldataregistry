from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DetailView
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from renaldataregistry.models import (
    PatientRegistration,
    Unit,
    Patient,
    PatientRenalDiagnosis,
    PatientAKImeasurement,
    PatientKRTModality,
    PatientAssessment,
    PatientLPAssessment,
    PatientMedicationAssessment,
    PatientStop,
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
)

# pylint: disable=too-many-statements, too-many-boolean-expressions, too-many-branches, too-many-lines

# Create your views here.
def load_units(request):
    "Get units of hospital"
    hi_id = request.GET.get("hi_id")
    units = Unit.objects.filter(healthinstitution=hi_id).order_by("name")
    return render(request, "unit_dropdownlist_options.html", {"units": units})


class PatientView(LoginRequiredMixin, DetailView):
    # This view shows the data entered in the patient registration form
    model = Patient
    template_name = "patient_view.html"

    def get_context_data(self, **kwargs):
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
        return context


class PatientRegistrationListView(LoginRequiredMixin, ListView):
    paginate_by = 15
    model = PatientRegistration
    count = 0

    def get_queryset(self):
        """
        Overwrites the get_query_set to add search option
        """
        try:
            search_word = self.request.GET.get(
                "search_keyword",
            )
        except KeyError:
            search_word = None

        if search_word:
            # Search by N.I.C or passport number, name, surname, health institution or unit.
            result_patients = PatientRegistration.objects.filter(
                Q(health_institution__name__icontains=search_word)
                | Q(unit__name__icontains=search_word)
                | Q(patient__name__icontains=search_word)
                | Q(patient__surname__icontains=search_word)
                | Q(patient__pid__icontains=search_word)
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
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context["search_word"] = self.request.GET.get("search_keyword")
            if context["search_word"]:
                context["count"] = self.count
        return context


class PatientRegistrationView(LoginRequiredMixin, UpdateView):
    def __init__(self):
        self.all_patient_krt_modalities = [None] * 6

    def get_krt_modalities(self, patient):
        """
        Get the patient's 6 oldest KRT modalities created in the registration form
        alternative to set all_patient_krt_modalities: see get_context_data of PatientView
        """
        left_krt_modalities_list = []
        i = 4
        # Loading chronology of KRT modalities (the 6 oldest ones) and sorting them in the relevant order for the patient registration form
        patient_krtmodalities = PatientKRTModality.objects.filter(
            patient=patient, created_at=patient.created_at
        ).order_by("start_date")[:6]

        # Rearranging krt modalities to meet chronology in patient registration form
        # is_first (for a krt modality) is only set in the patient's registration form
        for _, patientkrtmodality in enumerate(patient_krtmodalities):
            if patientkrtmodality.is_first:
                # setting first modality
                self.all_patient_krt_modalities[0] = patientkrtmodality
            else:
                if patientkrtmodality.is_current:
                    # setting current modality
                    self.all_patient_krt_modalities[5] = patientkrtmodality
                else:
                    # rest of the krt modalities
                    left_krt_modalities_list.append(patientkrtmodality)
        while left_krt_modalities_list:
            # merge rest of the krt modalities in the correspondant order
            self.all_patient_krt_modalities[i] = left_krt_modalities_list.pop()
            i -= 1

    def get(self, request, *args, **kwargs):
        context = {}
        template_name = "patient_register.html"
        title = "Patient registration form"

        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        if patient_id:
            # Add new patient
            patient = get_object_or_404(Patient, id=patient_id)
            context["patient"] = patient
            patient_form = PatientForm(instance=patient)
            patientregistration_form = PatientRegistrationForm(
                instance=patient.patientregistration
            )
            try:
                patientrenaldiagnosis_form = PatientRenalDiagnosisForm(
                    instance=patient.patientrenaldiagnosis
                )
            except PatientRenalDiagnosis.DoesNotExist:
                patientrenaldiagnosis_form = PatientRenalDiagnosisForm()

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
            patientrenaldiagnosis_form = PatientRenalDiagnosisForm()
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
        aki_saved = ""

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

            try:
                patientrenaldiagnosis_form = PatientRenalDiagnosisForm(
                    request.POST, instance=patient.patientrenaldiagnosis
                )
            except PatientRenalDiagnosis.DoesNotExist:
                patientrenaldiagnosis_form = PatientRenalDiagnosisForm(request.POST)

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
            patientrenaldiagnosis_form = PatientRenalDiagnosisForm(request.POST)

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
                patientrenaldiagnosis.save()

            # Registering the first KRT modality
            if any(
                item in patientkrtmodality_first_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_first = patientkrtmodality_first_form.save(
                    commit=False
                )
                patientkrtmodality_first.is_first = True
                patientkrtmodality_first.patient = patient
                patientkrtmodality_first.created_at = patient.created_at
                patientkrtmodality_first.save()

            # Registering the rest of the KRT modalities
            if any(
                item in patientkrtmodality_2_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_2 = patientkrtmodality_2_form.save(commit=False)
                patientkrtmodality_2.patient = patient
                patientkrtmodality_2.created_at = patient.created_at
                patientkrtmodality_2.save()

            if any(
                item in patientkrtmodality_3_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_3 = patientkrtmodality_3_form.save(commit=False)
                patientkrtmodality_3.patient = patient
                patientkrtmodality_3.created_at = patient.created_at
                patientkrtmodality_3.save()

            if any(
                item in patientkrtmodality_4_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_4 = patientkrtmodality_4_form.save(commit=False)
                patientkrtmodality_4.patient = patient
                patientkrtmodality_4.created_at = patient.created_at
                patientkrtmodality_4.save()

            if any(
                item in patientkrtmodality_5_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_5 = patientkrtmodality_5_form.save(commit=False)
                patientkrtmodality_5.patient = patient
                patientkrtmodality_5.created_at = patient.created_at
                patientkrtmodality_5.save()

            # Registering the current KRT modality
            if any(
                item in patientkrtmodality_present_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_present = patientkrtmodality_present_form.save(
                    commit=False
                )
                patientkrtmodality_present.is_current = True
                patientkrtmodality_present.patient = patient
                patientkrtmodality_present.created_at = patient.created_at
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
    model = PatientKRTModality
    template_name = "patientmodality_list.html"

    def get_queryset(self):
        """
        Overwrites the get_query_set to add search option
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
    def get(self, request, *args, **kwargs):
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

        return render(
            request,
            "patientmodality_view.html",
            context={
                "patientmodality": patientmodality,
                "patientakimeasurement": patientakimeasurement,
                "patient_assessement": patient_assessement,
            },
        )


class PatientModalityView(LoginRequiredMixin, UpdateView):
    # Register current patient's KRT modality
    def get(self, request, *args, **kwargs):
        template_name = "patient_modality.html"
        title = "Patient KRT modality form"
        krt_is_first = True

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
            if num_patientkrtmodalities > 0:
                krt_is_first = False
        else:
            if modality_id:
                # Edition of modality
                modality = get_object_or_404(PatientKRTModality, id=modality_id)
                patient = modality.patient

                krt_is_first = modality.is_first
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
                    patientkrtmodality.is_first = request.POST.get("krt_is_first")
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
                    modality = patientkrtmodality_form.save()

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
    model = PatientAssessment

    def get_context_data(self, **kwargs):
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

            all_patientassessments = PatientAssessment.objects.filter(
                patient=patient_id
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
    def get(self, request, *args, **kwargs):
        try:
            assessment_id = kwargs["assessment_id"]
        except KeyError:
            assessment_id = None

        patientassesment = get_object_or_404(PatientAssessment, pk=assessment_id)
        # patient = patientassesment.patient

        return render(
            request,
            "patientassessment_view.html",
            context={
                "patientassesment": patientassesment,
            },
        )


class PatientAssessmentView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
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
        context = {
            "patientkrtmodality_form": patientkrtmodality_form,
            "patientassessmentlp_form": patientassessmentlp_form,
            "patientassessmentmed_form": patientassessmentmed_form,
            "patientassessment_form": patientassessment_form,
            "view_title": title,
            "patient_current_krtmodality": patient_current_krtmodality,
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
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
        if (
            patientkrtmodality_form.is_valid()
            and patientassessmentlp_form.is_valid()
            and patientassessmentmed_form.is_valid()
            and patientassessment_form.is_valid()
        ):

            if patient_id:
                creation_date = timezone.now()

            # The KRT modality already exists, if there is any change, the krt modality is updated
            patientkrtmodality_form.save()

            patientassessment = patientassessment_form.save(commit=False)
            patientassessment.patient = patient
            if patient_id:
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
            messages.success(
                self.request,
                "Completed.",
                extra_tags="alert",
            )
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
        }
        return render(request, "patient_assess.html", context)


class PatientStopView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        title = "Patient stopping dialysis form"

        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        patient = get_object_or_404(Patient, id=patient_id)

        try:
            patientstop_form = PatientStopForm(instance=patient.patientstop)
        except PatientStop.DoesNotExist:
            patientstop_form = PatientStopForm()

        return render(
            request,
            "patient_stop.html",
            context={"patientstop_form": patientstop_form, "view_title": title},
        )

    def post(self, request, *args, **kwargs):
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
    def get(self, request, *args, **kwargs):
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
