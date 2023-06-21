from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, Profile
from django.contrib.auth.forms import UserChangeForm


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrong':
            raise ValidationError('Wrong password!')
        return data


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    photo = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'photo')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class ProfileEditForm(UserChangeForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(max_length=255, required=True)
    photo = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('user', 'photo')

    def save(self, commit=True):
        user = super().save(commit)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.photo = self.cleaned_data['photo']
        profile.save()
        return user

