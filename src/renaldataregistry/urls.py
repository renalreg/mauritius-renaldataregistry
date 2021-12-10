from django.urls import path

from .views import (
    PatientRegistrationListView,
    PatientRegistrationView,
    PatientAssessmentView,
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
        name="PatientRegistrationUpdateView",
    ),
    path(
        "patient/assess/",
        PatientAssessmentView.as_view(),
        name="PatientAssessmentView",
    ),
]
