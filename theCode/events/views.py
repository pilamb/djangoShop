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
    order               = Event
    template_name     = "events_list.html"
    paginate_by     = 4

    def get_notified_data(self, **kwargs):
            notified = super(EventListView, self).get_context_data(**kwargs)
            notified['today'] = date.today()
            return notified

    def get_queryset(self):
        return Event.objects.order_by('-date')
