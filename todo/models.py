# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    is_completed = models.BooleanField(default=False)
    content = models.TextField()
    assignee = models.ForeignKey(User, related_name="assignee")
    assignor = models.ForeignKey(User, related_name="assignor")


