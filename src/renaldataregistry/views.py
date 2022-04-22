from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
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

# pylint: disable=too-many-statements, too-many-boolean-expressions, too-many-branches

# Create your views here.
def load_units(request):
    "Get units of hospital"
    hi_id = request.GET.get("hi_id")
    units = Unit.objects.filter(healthinstitution=hi_id).order_by("name")
    return render(request, "unit_dropdownlist_options.html", {"units": units})


class PatientView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = "patient_view.html"


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
        Get the 6 oldest KRT modalities
        """
        left_krt_modalities_list = []
        i = 4
        # Loading chronology of KRT modalities (the 6 oldest ones) and sorting them in the relevant order for the patient registration form
        patient_krtmodalities = PatientKRTModality.objects.filter(
            patient=patient
        ).order_by("start_date")[:6]
        # Rearranging krt modalities to meet chronology in patient registration form
        for _, patientkrtmodality in enumerate(patient_krtmodalities):
            if patientkrtmodality.is_first and not patientkrtmodality.is_current:
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

        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None

        if patient_id:
            title = "Edit patient"
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

            # Choosing only the oldest created assessment since more assessments can be added in the Assessment form view
            patient_assessement = PatientAssessment.objects.filter(
                patient=patient
            ).order_by("created_at")[:1]
            patientassessment_form = PatientAssessmentForm(
                instance=patient_assessement[0]
            )
        else:
            title = "Register patient"
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
        first_krt = False

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

            # Choosing only the oldest created assessment since more assessments can be added in the Assessment form view
            patient_assessement = PatientAssessment.objects.filter(
                patient=patient
            ).order_by("created_at")[:1]
            patientassessment_form = PatientAssessmentForm(
                request.POST, instance=patient_assessement[0]
            )
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
            patientregistration.save()
            patientregistration_form.save_m2m()

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
                patientkrtmodality_first.save()
                first_krt = True

            # Registering the rest of the KRT modalities
            if any(
                item in patientkrtmodality_2_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_2 = patientkrtmodality_2_form.save(commit=False)
                patientkrtmodality_2.patient = patient
                patientkrtmodality_2.save()

            if any(
                item in patientkrtmodality_3_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_3 = patientkrtmodality_3_form.save(commit=False)
                patientkrtmodality_3.patient = patient
                patientkrtmodality_3.save()

            if any(
                item in patientkrtmodality_4_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_4 = patientkrtmodality_4_form.save(commit=False)
                patientkrtmodality_4.patient = patient
                patientkrtmodality_4.save()

            if any(
                item in patientkrtmodality_5_form.changed_data
                for item in ["modality", "start_date"]
            ):
                patientkrtmodality_5 = patientkrtmodality_5_form.save(commit=False)
                patientkrtmodality_5.patient = patient
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
                if not first_krt:
                    # current krt modality is also the first KRT modality
                    patientkrtmodality_present.is_first = True
                else:
                    # if first krt modality is now entered (for edition)
                    patientkrtmodality_present.is_first = False
                patientkrtmodality_present.patient = patient
                patientkrtmodality_present.save()

            if patient.in_krt_modality == "Y":
                patientakimeasurement_form = PatientAKIMeasurementForm()
                patientakimeasures = patientakimeasurement_form.save(commit=False)
                patientakimeasures.patient = patient
                patientakimeasures.save()
                aki_saved = " AKI measures are null because patient is in KRT."
            else:
                patientakimeasures = patientakimeasurement_form.save(commit=False)
                patientakimeasures.patient = patient
                patientakimeasures.save()

            patientassessment = patientassessment_form.save(commit=False)
            patientassessment.patient = patient
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


class PatientAssessmentView(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        patientkrtmodality_form = PatientKRTModalityForm()
        patientassessmentlp_form = PatientAssessmentLPForm()
        patientassessmentmed_form = PatientAssessmentMedicationForm()
        patientassessment_form = PatientAssessmentForm()
        context = {
            "patientkrtmodality_form": patientkrtmodality_form,
            "patientassessmentlp_form": patientassessmentlp_form,
            "patientassessmentmed_form": patientassessmentmed_form,
            "patientassessment_form": patientassessment_form,
        }
        return render(request, "patient_assess.html", context)


class PatientModalityView(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        patientkrtmodality_form = PatientKRTModalityForm()
        patientakimeasurement_form = PatientAKIMeasurementForm()
        context = {
            "patientkrtmodality_form": patientkrtmodality_form,
            "patientakimeasurement_form": patientakimeasurement_form,
        }
        return render(request, "patient_modality.html", context)


class PatientStopView(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        patientstop_form = PatientStopForm()
        context = {
            "patientstop_form": patientstop_form,
        }
        return render(request, "patient_stop.html", context)


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
