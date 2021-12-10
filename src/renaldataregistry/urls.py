from django.urls import path
from .views import RenalRegistryHomePageView


urlpatterns = [
    path("home/", RenalRegistryHomePageView.as_view(), name="renalregistry_home"),
]
