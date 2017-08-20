# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Notification


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls,**initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class NotificationDetailView(LoginRequiredMixin, DetailView):
    order = Notification
    template_name = "notifications/notification_detail.html"

    def get_object(self):
        object = super(NotificationDetailView, self).get_object()
        object.notified()
        object.save()
        return object


class NotificationListView(LoginRequiredMixin, ListView):
    order = Notification
    template_name = "notifications/notifications.html"

    def get_context_data(self, **kwargs):
        notified = super(NotificationListView, self).get_context_data(**kwargs)
        return notified

    def get_queryset(self):
        if not self.request.user.is_admin:
            return Notification.objects.filter(user=self.request.user)
        else:
            return Notification.objects.all()
