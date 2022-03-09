# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import PatientRegistration, Comorbidity
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group
from django import forms


User = get_user_model()


# Create ModelForm based on the Group model.
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("users", False),
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()
        self.save_m2m()
        return instance


admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ["permissions"]


# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)

admin.site.register(Comorbidity)

admin.site.register(PatientRegistration, SimpleHistoryAdmin)
