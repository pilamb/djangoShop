# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Evento
from django.views.generic.list import ListView
from django.views.generic import DetailView,  UpdateView, DeleteView
# from proyecto.views.crear_evento import Formulario_alta_evento
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from datetime import date

class EventoListView(ListView):
	order 		  	= Evento
	template_name 	= "listado_event.html"
	paginate_by 	= 4
	def get_connotified_data(self, **kwargs):
			connotified = super(EventoListView, self).get_connotified_data(**kwargs)
			connotified['hoy'] = date.today()
			return connotified
	def get_queryset(self):
		return Evento.objects.order_by('-date')