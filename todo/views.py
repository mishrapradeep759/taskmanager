# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.contrib.auth.models import User, Group
from .models import Profile
from .models import Task

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from todo.forms import TaskForm, LoginForm, RegistrationForm


def register_user(request):

    if request.method=="POST":
        registration_form = RegistrationForm(request.POST)

        if registration_form.is_valid():
            data = registration_form.cleaned_data
            email = data["email"]
            domain = email.split("@")[-1]
            group, created = Group.objects.get_or_create(name=domain)
            user = registration_form.save(commit=False)
            registration_form.save()
            profile = Profile.objects.create(user=user, group=group)

            # Group is created first time
            if created:
                profile.is_admin = True
                profile.is_active = True # if is_active is False, user can not login without admin approval
                profile.save()

            return redirect(reverse("todo:registered"))

    else:
        registration_form = RegistrationForm()
    return render(request, "todo/registration.html", {"registration_form": registration_form})


def user_login(request):

    if request.method=="POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            data = login_form.cleaned_data
            email = data["email"]
            password = data["password"]
            username = data["username"]
            user = authenticate(request, username=username, password=password)

            if user is not None:

                if user.profile.is_active:

                    login(request, user)
                    print user.profile.id

                    return redirect(reverse("todo:profile", args=(user.profile.id,)))

                else:
                    return HttpResponse("Login Request is pending for Approval")

    else:
        login_form = LoginForm()

    return render(request, "todo/login.html", {"form": login_form})


@login_required
def user_profile(request, user_id):
    profile = Profile.objects.get(pk=user_id)

    users = Profile.objects.filter(is_active=False, group=profile.group)
    admin_user = Profile.objects.get(is_admin=True, is_active=True, group=profile.group)

    return render(request, "todo/user.html", {"profiles": users, "admin_user": admin_user})


@login_required
def home_view(request):
    return render(request, "todo/home.html")


@login_required
def registered(request):
    return render(request, "todo/registration_completed.html")


@login_required
def get_pending_request(request):
    pending_requests = Profile.objects.filter(is_active=False)
    return render(request, "todo/pending_requests.html", {"pending_requests": pending_requests})


@login_required
def approve_user(request, user_id):

    user_profile = Profile.objects.get(user__id=user_id)
    user_profile.is_active=True
    user_profile.save()

    users = Profile.objects.filter(is_active=False, group=user_profile.group)
    admin_user = Profile.objects.get(is_admin=True, is_active=True, group=user_profile.group)

    return render(request, "todo/user.html", {"profiles": users, "admin_user": admin_user})


def home(request):
    return redirect(reverse("todo:logout"))


@login_required
def add_task(request):
    if request.method=="POST":
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            _form = form.save(commit=False)
            _form.assignor=request.user
            _form.save()
            return redirect(reverse("todo:taskboard"))
    else:
        form=TaskForm(request.user)
    return render(request, "todo/task.html", {"form": form})


@login_required
def taskboard(request):
    if request.user.profile.is_admin:
        tasks = Task.objects.filter(assignee__profile__group=request.user.profile.group)
    else:
        tasks = Task.objects.filter(assignee=request.user)
    context = {'tasks': tasks, 'user': request.user}
    return render(request, "todo/taskboard.html", context)


def get_user_email(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return user.email


def get_user(self, user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None


def create_user_domain(request, user_id):
    user_email = get_user_email(request, user_id)
    user_domain = user_email.split("@")[-1]
    return user_domain


def create_user_group(request):
    group = []
    users = User.objects.all()
    for user in users:
        group.append(create_user_domain(request, user.id))
    return render(request, "todo/group.html", {'group': group})

