# -*- coding: utf-8 -*-

from django.views.generic import DetailView, ListView
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

    def get_object(self):
        user_reads_it = super(NotificationDetailView, self).get_object()
        user_reads_it.seen()
        user_reads_it.save()
        return user_reads_it


class NotificationListView(LoginRequiredMixin, ListView):
    template_name = "notifications/notifications.html"

    def get_context_data(self, **kwargs):
        notified = super(NotificationListView, self).get_context_data(**kwargs)
        return notified

    def get_queryset(self):
        if not self.request.user.is_admin:
            return Notification.objects.filter(user=self.request.user)
        else:
            return Notification.objects.all()
