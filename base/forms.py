from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

        widgets = {
            "email" : forms.TextInput(attrs={"class":"form-control", "type":"email"}),
            "username" : forms.TextInput(attrs={"class":"form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ("user", "updated", "predicted_refill")

        widgets = {
            "pic" : forms.FileInput(attrs={"class":"form-control", "type":"file"}),
            "mobile_number" : forms.TextInput(attrs={"class":"form-control"}),
            "location" : forms.Select(attrs={"class":"form-select"}),
            "gas_brand" : forms.Select(attrs={"class":"form-select"}),
            "gas_size" : forms.Select(attrs={"class":"form-select"}),
            "married" : forms.CheckboxInput(attrs={"class":"form-check-input", "type":"checkbox"}),
            "household_number" : forms.TextInput(attrs={"class":"form-control"}),
            "kids_number" : forms.TextInput(attrs={"class":"form-control"}),
            "kids_below3" : forms.TextInput(attrs={"class":"form-control"}),
            "cooking_sequence" : forms.TextInput(attrs={"class":"form-control"}),
            "cooking_method" : forms.Select(attrs={"class":"form-control"}),
            "last_refill" : forms.TextInput(attrs={"class":"form-control", "type":"date"}),
        }



