from django.forms import Form
from likert_field.forms import LikertFormField
from django import forms
from .models import LecturerProfile
from django.contrib.auth.models import User


class CommentStars(Form):
    teaching_rate = LikertFormField()


class LecturerForm(forms.ModelForm):
    workPlaceName1 = forms.CharField(max_length=200, required=False, label='Nazwa Uczelni')
    workPlaceTown1 = forms.CharField(max_length=200, required=False, label='Miejscowość')
    workPlaceName2 = forms.CharField(max_length=200, required=False, label='Nazwa Uczelni')
    workPlaceTown2 = forms.CharField(max_length=200, required=False, label='Miejscowość')
    workPlaceName3 = forms.CharField(max_length=200, required=False, label='Nazwa Uczelni')
    workPlaceTown3 = forms.CharField(max_length=200, required=False, label='Miejscowość')
    tag1 = forms.CharField(max_length=200, required=False, label='Dziedzina')
    tag2 = forms.CharField(max_length=200, required=False, label='Dziedzina')
    tag3 = forms.CharField(max_length=200, required=False, label='Dziedzina')

    class Meta:
        model = LecturerProfile
        exclude = ['user_id', 'work_places', 'tags', 'knowledge_av', 'teaching_av', 'friendliness_av']


class RegistrationForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True, label='Adres email')

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined']