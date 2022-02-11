from django.urls import path

from .views import (
    PatientRegistrationListView,
    PatientRegistrationView,
    PatientAssessmentView,
    PatientModalityView,
    PatientStopView,
    PatientRegistrationUpdateView,
)

app_name = "renaldataregistry"

urlpatterns = [
    path(
        "patientregistration/list/",
        PatientRegistrationListView.as_view(),
        name="PatientRegistrationListView",
    ),
    path(
        "patient/register/",
        PatientRegistrationView.as_view(),
        name="PatientRegistrationView",
    ),
    path(
        "patient/<int:patient_id>/edit/",
        PatientRegistrationView.as_view(),
        name="PatientUpdateView",
    ),
    path(
        "patient/assess/",
        PatientAssessmentView.as_view(),
        name="PatientAssessmentView",
    ),
    path(
        "patient/krtmodality/",
        PatientModalityView.as_view(),
        name="PatientModalityView",
    ),
    path(
        "patient/stopdialysis/",
        PatientStopView.as_view(),
        name="PatientStopView",
    ),
    path(
        "patientregistration/<int:patient_id>/update/",
        PatientRegistrationUpdateView.as_view(),
        name="PatientRegistrationUpdateView",
    ),
]
