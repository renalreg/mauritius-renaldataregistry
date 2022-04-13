from typing import List

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom user admin where email is the unique identifier
    for authentication instead of usernames.
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_per_page = 15
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Name", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            "User account",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    search_fields = ("email",)
    ordering = ("email",)


# Create ModelForm based on the Group model.
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude: List[str] = []

    User = get_user_model()
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # type: ignore
        required=False,
        widget=FilteredSelectMultiple("users", False),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):  # pylint: disable=E0202
        """Add set of users"""
        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        """Save group"""
        instance = super().save()
        self.save_m2m()
        return instance


admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ["permissions"]


# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)
