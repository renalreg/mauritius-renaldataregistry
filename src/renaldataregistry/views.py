from django.forms import inlineformset_factory
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
    PatientKRTModalityFormSet,
    PatientKRTModalityForm,
)

# pylint: disable=too-many-statements
# pylint: disable=too-many-boolean-expressions

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

            existing_krtmodalities = patient.patientkrtmodality_set.count()
            patientkrtmodality_iformset = inlineformset_factory(
                Patient,
                PatientKRTModality,
                form=PatientKRTModalityForm,
                extra=6 - existing_krtmodalities,
                can_delete=False,
            )
            patientkrtmodality_forms = patientkrtmodality_iformset(instance=patient)

            try:
                patientakimeasurement_form = PatientAKIMeasurementForm(
                    instance=patient.patientakimeasurement
                )
            except PatientAKImeasurement.DoesNotExist:
                patientakimeasurement_form = PatientAKIMeasurementForm()

            patient_assessement = PatientAssessment.objects.get(patient=patient)
            patientassessment_form = PatientAssessmentForm(instance=patient_assessement)
        else:
            title = "Register patient"
            patientregistration_form = PatientRegistrationForm()
            patient_form = PatientForm()
            patientrenaldiagnosis_form = PatientRenalDiagnosisForm()
            patientkrtmodality_forms = PatientKRTModalityFormSet()
            patientakimeasurement_form = PatientAKIMeasurementForm()
            patientassessment_form = PatientAssessmentForm()
        context = {
            "patientregistration_form": patientregistration_form,
            "patient_form": patient_form,
            "patientrenaldiagnosis_form": patientrenaldiagnosis_form,
            "patientkrtmodality_forms": patientkrtmodality_forms,
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
            # existing patient
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

            patientkrtmodality_forms = PatientKRTModalityFormSet(
                request.POST, instance=patient
            )
            try:
                patientakimeasurement_form = PatientAKIMeasurementForm(
                    request.POST, instance=patient.patientakimeasurement
                )
            except PatientAKImeasurement.DoesNotExist:
                patientakimeasurement_form = PatientAKIMeasurementForm(request.POST)

            patient_assessement = PatientAssessment.objects.get(patient=patient)
            patientassessment_form = PatientAssessmentForm(
                request.POST, instance=patient_assessement
            )
        else:
            # new patient
            patientregistration_form = PatientRegistrationForm(request.POST)
            patient_form = PatientForm(request.POST)
            patientrenaldiagnosis_form = PatientRenalDiagnosisForm(request.POST)
            patientkrtmodality_forms = PatientKRTModalityFormSet(request.POST)
            patientakimeasurement_form = PatientAKIMeasurementForm(request.POST)
            patientassessment_form = PatientAssessmentForm(request.POST)
        if (
            patient_form.is_valid()
            and patientregistration_form.is_valid()
            and patientrenaldiagnosis_form.is_valid()
            and patientakimeasurement_form.is_valid()
            and patientkrtmodality_forms.is_valid()
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

            patientkrtmodalities = patientkrtmodality_forms.save(commit=False)
            for patientkrtmodality in patientkrtmodalities:
                patientkrtmodality.patient = patient
                patientkrtmodality.save()

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
            "patientkrtmodality_forms": patientkrtmodality_forms,
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
