from django.contrib.auth import forms
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, reverse, redirect, get_object_or_404

from .models import Group
from .models import Task, Profile



class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError(
                "This email address is already in use. Please supply a different email address."
            )
        return self.cleaned_data['email']

    def save(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        data = RegistrationForm.cleaned_data
        email = data["email"]
        domain = email.split("@")[-1]
        group, created = Group.objects.get_or_create(name=domain)
        user = RegistrationForm.save(commit=False)
        RegistrationForm.save()
        profile = Profile.objects.create(user=user, group=group)

        # If Group is created first time
        if created:
            profile.is_admin = True
            profile.is_active = True  # if is_active is False, user can not login without admin approval
            profile.save()


class LoginForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        username, password, email = (data["username"], data["password"], data["email"])
        self.user = authenticate(username=username, password=password)

        if self.user is None:

            raise forms.ValidationError(
                "Enter a valid email or password"
            )


class TaskForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        self.fields["assignee"].queryset = User.objects.filter(
            profile__group=user.profile.group,
            profile__is_active=True
        )

    class Meta:
        model = Task
        fields=(
            "content",
            "assignee",
        )