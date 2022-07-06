"""mauritiusrenalregistry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (
    PatientRegistrationListView,
    PatientRegistrationView,
    PatientStopView,
    PatientRegistrationHistoryView,
    PatientView,
    PatientModalityListView,
    PatientModalityView,
    PatientAssessmentListView,
    PatientAssessmentView,
    PatientModalityDetailView,
    PatientAssessmentDetailView,
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
        "patientregistration/<int:patient_id>/viewhistory/",
        PatientRegistrationHistoryView.as_view(),
        name="PatientRegistrationHistoryView",
    ),
    path(
        "patient/<pk>/view/",
        PatientView.as_view(),
        name="PatientRecordView",
    ),
    path(
        "patientmodality/<int:patient_id>/list/",
        PatientModalityListView.as_view(),
        name="PatientModalityListView",
    ),
    path(
        "patient/<int:patient_id>/modality/",
        PatientModalityView.as_view(),
        name="PatientModalityView",
    ),
    path(
        "patientmodality/<int:modality_id>/edit/",
        PatientModalityView.as_view(),
        name="PatientModalityUpdateView",
    ),
    path(
        "patientassessment/<int:patient_id>/list/",
        PatientAssessmentListView.as_view(),
        name="PatientAssessmentListView",
    ),
    path(
        "patient/<int:patient_id>/assess/",
        PatientAssessmentView.as_view(),
        name="PatientAssessmentView",
    ),
    path(
        "patientassessment/<int:assessment_id>/edit/",
        PatientAssessmentView.as_view(),
        name="PatientAssessmentUpdateView",
    ),
    path(
        "patient/<int:patient_id>/stopdialysis/",
        PatientStopView.as_view(),
        name="PatientStopUpdateView",
    ),
    path(
        "patientmodality/<int:modality_id>/view/",
        PatientModalityDetailView.as_view(),
        name="PatientModalityDetailView",
    ),
    path(
        "patientassessment/<int:assessment_id>/view/",
        PatientAssessmentDetailView.as_view(),
        name="PatientAssessmentDetailView",
    ),
]
