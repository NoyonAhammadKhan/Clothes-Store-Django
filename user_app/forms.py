from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email',]


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email']
