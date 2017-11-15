# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Event
from django.views.generic.list import ListView
from django.views.generic import DetailView,  UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from datetime import date


class EventListView(ListView):
    """
    This view is enough since only admins can post events.
    """
    model = Event
    template_name = "events/events_list.html"
    paginate_by = 4

    def get_notified_data(self, *args):
        notified = super(EventListView, self).get_context_data(*args)
        notified['today'] = date.today()
        return notified

    def get_queryset(self):
        return Event.objects.all().order_by('-begin_date')

# TODO: detailView