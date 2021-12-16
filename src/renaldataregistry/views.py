import pdb

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView

from renaldataregistry.forms import (
    PatientAddressForm,
    PatientAKIMeasurement,
    PatientAssessmentForm,
    PatientAssessmentLPForm,
    PatientAssessmentMedicationForm,
    PatientContactForm,
    PatientContactFormSet,
    PatientForm,
    PatientKRTModalityForm,
    PatientMeasurementForm,
    PatientOccupationForm,
    PatientRegistrationForm,
)
from renaldataregistry.models import (
    LaboratoryParameter,
    Patient,
    PatientAddress,
    PatientRegistration,
)


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
            print(type(search_word))
            # Search by N.I.C or passport number, name, surname, health institution or unit.
            result_patients = PatientRegistration.objects.filter(
                Q(unit__name__icontains=search_word)
                | Q(patient__name__icontains=search_word)
            )
            self.count = result_patients.count()
            return result_patients
        else:
            all_patientregistrations = PatientRegistration.objects.prefetch_related(
                "patient"
            ).all()
            self.count = all_patientregistrations.count()
            return all_patientregistrations


class PatientRegistrationView(LoginRequiredMixin, UpdateView):
    def get(self, request, patient_id=None):
        try:
            patient_id = self.kwargs["patient_id"]
        except KeyError:
            patient_id = None
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
            patient_form = PatientForm(instance=patient)
            try:
                patientregistration_form = PatientRegistrationForm(
                    instance=patient.patientregistration
                )
                patientaddress_form = PatientAddressForm(
                    instance=patient.patientaddress
                )
            except PatientRegistration.DoesNotExist:
                patientregistration_form = PatientRegistrationForm()
            except PatientAddress.DoesNotExist:
                patientaddress_form = PatientAddressForm()
            template_name = "patient_edit.html"
            context = {
                "patient": patient,
                "patient_form": patient_form,
                "patientregistration_form": patientregistration_form,
                "patientaddress_form": patientaddress_form,
            }
        else:
            patientregistration_form = PatientRegistrationForm()
            patient_form = PatientForm()
            patientaddress_form = PatientAddressForm()
            patientcontact_forms = PatientContactFormSet()
            patientmeasurement_form1 = PatientMeasurementForm(auto_id="height_%s")
            patientmeasurement_form2 = PatientMeasurementForm(auto_id="weight_%s")
            patientmeasurement_form3 = PatientMeasurementForm(auto_id="birthweight_%s")
            patientoccupation_form1 = PatientOccupationForm(auto_id="currentemp_%s")
            patientoccupation_form2 = PatientOccupationForm(auto_id="prevemp1_%s")
            patientoccupation_form3 = PatientOccupationForm(auto_id="prevemp2_%s")
            patientoccupation_form4 = PatientOccupationForm(auto_id="prevemp3_%s")
            patientoccupation_form5 = PatientOccupationForm(auto_id="prevemp4_%s")
            patientkrtmodality_form1 = PatientKRTModalityForm(
                auto_id="initialKRTmod_%s"
            )
            patientkrtmodality_form2 = PatientKRTModalityForm(auto_id="otherKRTmod1_%s")
            patientkrtmodality_form3 = PatientKRTModalityForm(auto_id="otherKRTmod2_%s")
            patientkrtmodality_form4 = PatientKRTModalityForm(auto_id="otherKRTmod3_%s")
            patientkrtmodality_form5 = PatientKRTModalityForm(auto_id="otherKRTmod4_%s")
            patientkrtmodality_form6 = PatientKRTModalityForm(
                auto_id="currentKRTmod_%s"
            )
            patientakimeasurement_form = PatientAKIMeasurement()
            patientassessment_form = PatientAssessmentForm()
            context = {
                "patientregistration_form": patientregistration_form,
                "patient_form": patient_form,
                "patientaddress_form": patientaddress_form,
                "patientcontact_forms": patientcontact_forms,
                "patientmeasurement_form1": patientmeasurement_form1,
                "patientmeasurement_form2": patientmeasurement_form2,
                "patientmeasurement_form3": patientmeasurement_form3,
                "patientoccupation_form1": patientoccupation_form1,
                "patientoccupation_form2": patientoccupation_form2,
                "patientoccupation_form3": patientoccupation_form3,
                "patientoccupation_form4": patientoccupation_form4,
                "patientoccupation_form5": patientoccupation_form5,
                "patientkrtmodality_form1": patientkrtmodality_form1,
                "patientkrtmodality_form2": patientkrtmodality_form2,
                "patientkrtmodality_form3": patientkrtmodality_form3,
                "patientkrtmodality_form4": patientkrtmodality_form4,
                "patientkrtmodality_form5": patientkrtmodality_form5,
                "patientkrtmodality_form6": patientkrtmodality_form6,
                "patientakimeasurement_form": patientakimeasurement_form,
                "patientassessment_form": patientassessment_form,
            }
            template_name = "patient_register.html"
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        patientregistration_form = PatientRegistrationForm(request.POST)
        patient_form = PatientForm(request.POST)
        patientaddress_form = PatientAddressForm(request.POST)
        patientcontact_form1 = PatientContactForm(request.POST)
        patientcontact_form2 = PatientContactForm(request.POST)
        patientcontact_form3 = PatientContactForm(request.POST)
        patientcontact_form4 = PatientContactForm(request.POST)
        patientcontact_form5 = PatientContactForm(request.POST)
        patientcontact_form6 = PatientContactForm(request.POST)
        patientmeasurement_form1 = PatientMeasurementForm(request.POST)
        patientmeasurement_form2 = PatientMeasurementForm(request.POST)
        patientmeasurement_form3 = PatientMeasurementForm(request.POST)
        patientoccupation_form1 = PatientOccupationForm(request.POST)
        patientoccupation_form2 = PatientOccupationForm(request.POST)
        patientoccupation_form3 = PatientOccupationForm(request.POST)
        patientoccupation_form4 = PatientOccupationForm(request.POST)
        patientoccupation_form5 = PatientOccupationForm(request.POST)
        patientkrtmodality_form1 = PatientKRTModalityForm(request.POST)
        patientkrtmodality_form2 = PatientKRTModalityForm(request.POST)
        patientkrtmodality_form3 = PatientKRTModalityForm(request.POST)
        patientkrtmodality_form4 = PatientKRTModalityForm(request.POST)
        patientkrtmodality_form5 = PatientKRTModalityForm(request.POST)
        patientkrtmodality_form6 = PatientKRTModalityForm(request.POST)
        patientakimeasurement_form = PatientAKIMeasurement(request.POST)
        patientassessment_form = PatientAssessmentForm(request.POST)

        pdb.set_trace()

        if (
            patient_form.is_valid()
            and patientregistration_form.is_valid()
            and patientcontact_form1.is_valid()
        ):
            patient = patient_form.save(commit=False)
            # patient.save()

            patientregistration = patientregistration_form.save(commit=False)
            patientregistration.patient = patient
            # patientregistration.save()

            patientcontactform1 = patientcontact_form1.save(commit=False)
            patientcontactform1.patient = patient

            if (
                patientcontact_form1.instance.patientcontact_set - 0 - contactvalue
                is not None
            ):
                patientcontact_form1.instance.contactchannel = "P"
            # patientcontactform1.save()

            messages.success(
                self.request,
                "Completed - new patient added",
                extra_tags="alert",
            )
            return redirect("renaldataregistry:PatientRegistrationListView")
        else:
            messages.error(
                self.request,
                "Patient creation failed - see below",
                extra_tags="alert",
            )
            context = {
                "patientregistration_form": patientregistration_form,
                "patient_form": patient_form,
                "patientaddress_form": patientaddress_form,
                "patientcontact_form1": patientcontact_form1,
                "patientcontact_form2": patientcontact_form2,
                "patientcontact_form3": patientcontact_form3,
                "patientcontact_form4": patientcontact_form4,
                "patientcontact_form5": patientcontact_form5,
                "patientcontact_form6": patientcontact_form6,
                "patientmeasurement_form1": patientmeasurement_form1,
                "patientmeasurement_form2": patientmeasurement_form2,
                "patientmeasurement_form3": patientmeasurement_form3,
                "patientoccupation_form1": patientoccupation_form1,
                "patientoccupation_form2": patientoccupation_form2,
                "patientoccupation_form3": patientoccupation_form3,
                "patientoccupation_form4": patientoccupation_form4,
                "patientoccupation_form5": patientoccupation_form5,
                "patientkrtmodality_form1": patientkrtmodality_form1,
                "patientkrtmodality_form2": patientkrtmodality_form2,
                "patientkrtmodality_form3": patientkrtmodality_form3,
                "patientkrtmodality_form4": patientkrtmodality_form4,
                "patientkrtmodality_form5": patientkrtmodality_form5,
                "patientkrtmodality_form6": patientkrtmodality_form6,
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
