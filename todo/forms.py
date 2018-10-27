from django.contrib.auth import forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput)


class TaskForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        self.fields["assignee"].queryset = User.objects.filter(profile__group=user.profile.group)

    class Meta:
        model = Task
        fields=("content", "assignee",)