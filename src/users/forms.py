from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email",)

    def clean_email(self):
        data = self.cleaned_data["email"]
        return data.lower()


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

    def clean_email(self):
        data = self.cleaned_data["email"]
        return data.lower()
