from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        return super(LoginView, self).get(request, *args, **kwargs)
