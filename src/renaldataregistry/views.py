from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from renaldataregistry.models import (
    PatientRegistration,
    Patient,
    PatientAddress,
    PatientContact,
    PatientRenalDiagnosis,
    PatientAKImeasurement,
    PatientMeasurement,
)
from renaldataregistry.forms import (
    PatientRegistrationForm,
    PatientForm,
    PatientAddressForm,
    PatientRenalDiagnosisForm,
    PatientAKIMeasurementForm,
    PatientAssessmentForm,
    PatientAssessmentLPForm,
    PatientAssessmentMedicationForm,
    PatientContactFormSet,
    PatientStopForm,
    PatientMeasurementFormSet,
    PatientOccupationFormSet,
    PatientKRTModalityFormSet,
    PatientKRTModalityForm,
    CustomInlineFormSet,
    PatientContactForm,
    CustomMeasurementInlineFormSet,
    PatientMeasurementForm,
)

# pylint: disable=too-many-statements
# pylint: disable=too-many-boolean-expressions

# Create your views here.
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
                Q(unit__name__icontains=search_word)
                | Q(patient__name__icontains=search_word)
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
            patient = get_object_or_404(Patient, id=patient_id)
            context["patient"] = patient
            patient_form = PatientForm(instance=patient)
            patientregistration_form = PatientRegistrationForm(
                instance=patient.patientregistration
            )
            try:
                patientaddress_form = PatientAddressForm(
                    instance=patient.patientaddress
                )
            except PatientAddress.DoesNotExist:
                patientaddress_form = PatientAddressForm()

            # maxcontacts (6)
            patientcontact_iformset = inlineformset_factory(
                Patient,
                PatientContact,
                form=PatientContactForm,
                formset=CustomInlineFormSet,
                extra=6 - patient.patientcontact_set.count(),
            )
            patientcontact_forms = patientcontact_iformset(instance=patient)

            # max measures (3)
            existing_measures = patient.patientmeasurement_set.count()
            patientmeasurement_iformset = inlineformset_factory(
                Patient,
                PatientMeasurement,
                form=PatientMeasurementForm,
                formset=CustomMeasurementInlineFormSet,
                extra=3 - existing_measures,
                can_delete=False,
            )
            patientmeasurement_forms = patientmeasurement_iformset(
                instance=patient,
                initial=[
                    {"measurementtype": 1},
                    {"measurementtype": 2},
                    {"measurementtype": 3},
                ],
            )
            patientoccupation_forms = PatientOccupationFormSet(instance=patient)

            try:
                patientrenaldiagnosis_form = PatientRenalDiagnosisForm(
                    instance=patient.patientrenaldiagnosis
                )
            except PatientRenalDiagnosis.DoesNotExist:
                patientrenaldiagnosis_form = PatientRenalDiagnosisForm()

            patientkrtmodality_forms = PatientKRTModalityFormSet(instance=patient)

            try:
                patientakimeasurement_form = PatientAKIMeasurementForm(
                    instance=patient.patientakimeasurement
                )
            except PatientAKImeasurement.DoesNotExist:
                patientakimeasurement_form = PatientAKIMeasurementForm()

            patientassessment_form = PatientAssessmentForm(instance=patient)
        else:
            patientregistration_form = PatientRegistrationForm()
            patient_form = PatientForm()
            patientaddress_form = PatientAddressForm()
            patientcontact_forms = PatientContactFormSet()
            patientmeasurement_forms = PatientMeasurementFormSet(
                initial=[
                    {"measurementtype": 1},
                    {"measurementtype": 2},
                    {"measurementtype": 3},
                ]
            )
            patientoccupation_forms = PatientOccupationFormSet()
            patientrenaldiagnosis_form = PatientRenalDiagnosisForm()
            patientkrtmodality_forms = PatientKRTModalityFormSet()
            patientakimeasurement_form = PatientAKIMeasurementForm()
            patientassessment_form = PatientAssessmentForm()
        context = {
            "patientregistration_form": patientregistration_form,
            "patient_form": patient_form,
            "patientaddress_form": patientaddress_form,
            "patientcontact_forms": patientcontact_forms,
            "patientmeasurement_forms": patientmeasurement_forms,
            "patientoccupation_forms": patientoccupation_forms,
            "patientrenaldiagnosis_form": patientrenaldiagnosis_form,
            "patientkrtmodality_forms": patientkrtmodality_forms,
            "patientakimeasurement_form": patientakimeasurement_form,
            "patientassessment_form": patientassessment_form,
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
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
                patientaddress_form = PatientAddressForm(
                    request.POST, instance=patient.patientaddress
                )
            except PatientAddress.DoesNotExist:
                patientaddress_form = PatientAddressForm(request.POST)

            patientcontact_forms = PatientContactFormSet(request.POST, instance=patient)
            patientmeasurement_forms = PatientMeasurementFormSet(
                request.POST, instance=patient
            )
            patientoccupation_forms = PatientOccupationFormSet(
                request.POST, instance=patient
            )
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
            patientassessment_form = PatientAssessmentForm(
                request.POST, instance=patient
            )
        else:
            # new patient
            patientregistration_form = PatientRegistrationForm(request.POST)
            patient_form = PatientForm(request.POST)
            patientaddress_form = PatientAddressForm(request.POST)
            patientcontact_forms = PatientContactFormSet(request.POST)
            patientmeasurement_forms = PatientMeasurementFormSet(request.POST)
            patientoccupation_forms = PatientOccupationFormSet(request.POST)
            patientrenaldiagnosis_form = PatientRenalDiagnosisForm(request.POST)
            patientkrtmodality_forms = PatientKRTModalityFormSet(request.POST)
            patientakimeasurement_form = PatientAKIMeasurementForm(request.POST)
            patientassessment_form = PatientAssessmentForm(request.POST)

        if (
            patient_form.is_valid()
            and patientregistration_form.is_valid()
            and patientaddress_form.is_valid()
            and patientcontact_forms.is_valid()
            and patientmeasurement_forms.is_valid()
            and patientakimeasurement_form.is_valid()
        ):
            patient = patient_form.save()

            if patientregistration_form.has_changed():
                patientregistration = patientregistration_form.save(commit=False)
                patientregistration.patient = patient
                patientregistration.save()

            if patientaddress_form.has_changed():
                patientaddress = patientaddress_form.save(commit=False)
                patientaddress.patient = patient
                patientaddress.save()

            patientcontacts = patientcontact_forms.save(commit=False)
            for patientcontact in patientcontacts:
                patientcontact.patient = patient
                patientcontact.save()

            patientmeasurements = patientmeasurement_forms.save(commit=False)
            for patientmeasurement in patientmeasurements:
                patientmeasurement.patient = patient
                patientmeasurement.save()

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
        context = {
            "patientregistration_form": patientregistration_form,
            "patient_form": patient_form,
            "patientaddress_form": patientaddress_form,
            "patientcontact_forms": patientcontact_forms,
            "patientmeasurement_forms": patientmeasurement_forms,
            "patientoccupation_forms": patientoccupation_forms,
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


class PatientRegistrationUpdateView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
            try:
                patientregistration_form = PatientRegistrationForm(
                    instance=patient.patientregistration
                )
            except PatientRegistration.DoesNotExist:
                patientregistration_form = PatientRegistrationForm()
            context = {
                "patient": patient,
                "patientregistration_form": patientregistration_form,
            }
            return render(request, "patientregistration_edit.html", context)
        return redirect("renaldataregistry:PatientRegistrationListView")

    def post(self, request, *args, **kwargs):
        try:
            patient_id = kwargs["patient_id"]
        except KeyError:
            patient_id = None
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
            patientregistration_form = PatientRegistrationForm(
                request.POST, instance=patient.patientregistration
            )
            if patientregistration_form.is_valid():
                patientregistration_form.save()
                messages.success(
                    self.request,
                    "Completed - patient main unit updated.",
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
        }
        return render(request, "patientregistration_edit.html", context)
