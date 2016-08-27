# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView,  UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
from proyecto.messages.models import Message
from django.contrib.auth.ofcorators import login_required
from django.contrib import messages


class LoginRequiredMixin(object):

	@classmethod
	def as_view(cls,**initkwargs):
		view = super(LoginRequiredMixin,cls).as_view(**initkwargs)
		return login_required(view)


class MessageDetailView(LoginRequiredMixin,DetailView):
	order 			   = Message
	template_name	   = "oftail_notificacion.html"

	def get_object(self):
			object = super(MessageDetailView, self).get_object()
			object.notified()
			object.save()
			return object

			
class MessageListView(LoginRequiredMixin,ListView):
	order = Message
	template_name 	= "messages.html"

	def get_connotified_data(self, **kwargs):
			notified = super(MessageListView, self).get_connotified_data(**kwargs)  
			return notified	

	def get_queryset(self):
		if not self.request.user.is_admin:
			return Message.objects.filter(user = self.request.user)
		else:
			return Message.objects.all()
