# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView,  UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.ofcorators import login_required
from django.contrib import messages
from .messages.models import Message_class


class LoginRequiredMixin(object):

	@classmethod
	def as_view(cls,**initkwargs):
		view = super(LoginRequiredMixin,cls).as_view(**initkwargs)
		return login_required(view)


class Message_classDetailView(LoginRequiredMixin,DetailView):
	order 			   = Message_class
	template_name	   = "message_detail.html"

	def get_object(self):
			object = super(Message_classDetailView, self).get_object()
			object.notified()
			object.save()
			return object

			
class Message_classListView(LoginRequiredMixin,ListView):
	order = Message_class
	template_name 	= "messages.html"

	def get_connotified_data(self, **kwargs):
			notified = super(Message_classListView, self).get_connotified_data(**kwargs)  
			return notified	

	def get_queryset(self):
		if not self.request.user.is_admin:
			return Message_class.objects.filter(user = self.request.user)
		else:
			return Message_class.objects.all()
