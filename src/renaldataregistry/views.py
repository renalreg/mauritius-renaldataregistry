from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.


@method_decorator(ensure_csrf_cookie, "get")
class RenalRegistryHomePageView(LoginRequiredMixin, TemplateView):
    template_name = "renalregistry_home.html"
