# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from .models import Notification


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = "notifications/notification_detail.html"


class NotificationListView(LoginRequiredMixin, ListView):
    order = Notification
    template_name = "notifications/notifications.html"

    def get_queryset(self):
        if not self.request.user.is_admin:
            return Notification.objects.filter(user=self.request.user)
        else:
            return Notification.objects.all()
