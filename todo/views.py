# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.contrib.auth.models import User, Group
from django.db.models import Q
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login

from .models import Profile
from .models import Task

from todo.forms import TaskForm, LoginForm, RegistrationForm


def registration(request):

    if request.POST:
        registration_form = RegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()
            return redirect(reverse("todo:registered"))

    else:
        registration_form = RegistrationForm()
    return render(request, "todo/registration.html", {"registration_form": registration_form})


def login_view(request):

    if not request.user.is_authenticated:
        if request.POST:
            login_form = LoginForm(request.POST)

            if login_form.is_valid():

                if login_form.user.profile.is_active:

                    auth_login(request, login_form.user)

                    return redirect(reverse("todo:profile", args=(login_form.user.profile.id,)))

                else:
                    return HttpResponse("Hi %s, Your Login Request is pending for Approval"
                                        % login_form.user.username.title())
        else:
            login_form = LoginForm()

        return render(request, "todo/login.html", {"form": login_form, "error": ""})
    else:
        return redirect(reverse("todo:profile", args=(request.user.profile.id,)))


@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.POST:
        form = TaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            form = form.save(commit=False)
            form.assignor=request.user
            form.assignee=task.assignee
            form.save()
            return redirect(reverse("todo:taskboard"))
    else:
        form=TaskForm(request.user, instance=task)
    return render(request, "todo/task.html", {"form": form})

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect(reverse("todo:taskboard"))


@login_required
def user_profile(request, user_id):
    profile = get_object_or_404(Profile, pk=user_id)

    users = Profile.objects.filter(
        is_active=False, group=profile.group
    )

    admin_user = get_object_or_404(
        Profile, is_admin=True, is_active=True,
        group=profile.group
    )

    return render(request, "todo/user.html",
                  {"profiles": users, "admin_user": admin_user})


@login_required
def home_view(request):
    return render(request, "todo/home.html")

def registered(request):
    return render(request, "todo/registration_completed.html")


@login_required
def get_pending_request(request):
    pending_requests = Profile.objects.filter(is_active=False)
    return render(request, "todo/pending_requests.html",
                  {"pending_requests": pending_requests})


@login_required
def approve_user(request, user_id):

    user_profile = Profile.objects.get(user__id=user_id)
    user_profile.is_active=True
    user_profile.save()

    users = Profile.objects.filter(
        is_active=False, group=user_profile.group
    )
    admin_user = get_object_or_404(
        Profile, is_admin=True, is_active=True,
        group=user_profile.group
    )

    return render(request, "todo/user.html",
                  {"profiles": users, "admin_user": admin_user})


@login_required
def add_task(request):
    if request.POST:
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.assignor=request.user
            form.save()
            return redirect(reverse("todo:profile", args=(request.user.profile.id,)))
    else:
        form=TaskForm(request.user)
    return render(request, "todo/task.html", {"form": form})


@login_required
def taskboard(request):
    if request.user.profile.is_admin:
        tasks = Task.objects.filter(assignee__profile__group=request.user.profile.group)
    else:
        tasks = Task.objects.filter(Q(assignee=request.user, is_completed=False) |
                                    Q(assignor=request.user))

    context = {'tasks': tasks, 'user': request.user}

    return render(request, "todo/taskboard.html", context)


@login_required
def task_completed(request, task_id):
    task = Task.objects.get(id=task_id, assignee=request.user)
    task.is_completed = True
    task.save()
    return redirect(reverse("todo:taskboard"))



# Basic helper functions

def get_user_email(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return user.email

def get_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return user

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

@login_required
def home(request):
    return redirect(reverse("todo:logout"))


def get_user_profile(request, user):
    if user.profile.is_active:

        auth_login(request, user)

        return redirect(reverse("todo:profile", args=(user.profile.id,)))

    else:
        return HttpResponse("Hi %s, Your Login Request is pending for Approval" % user.username.title())

