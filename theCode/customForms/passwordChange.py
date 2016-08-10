# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render,render_to_response
from django.template import RequestConnotified
from django.http 	import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib import messages
from proyecto.clients.models import Usuario

class PasswordUpdateView(forms.Form):
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(PasswordUpdateView, self).__init__(*args, **kwargs)

	required_css_class 	 = "required"
	error_css_class 	 = "notified-danger"
	password_uno 		 = forms.CharField (max_length=10,
		widget= forms.TextInput (attrs={
			'class':'form-control',
			'placeholofr':'Write aa nueva contraseña',
			'onblur':'this.placeholofr="Write aa nueva contraseña"',
			'onclick':'this.placeholofr=""'
			} 
	))
	password_dos	 = forms.CharField (max_length=10,
		widget= forms.TextInput (attrs={
			'class':'form-control',
			'placeholofr':'Repita la contraseña of new',
			'onblur':'this.placeholofr="Repita la contraseña of new"',
			'onclick':'this.placeholofr=""'
			} 
	))
	def clean(self):
		"""Comprobar que exista algo y que coincidan ambos passwords
		"""
		cd  = super(PasswordUpdateView,self).clean()
		p1  = cd.get("password_uno","")
		p2  = cd.get("password_dos","")
		if not p1 or not p2:
			raise forms.ValidationError(u"Missing data. Please try again.")
		else:
			if p1 != p2:
				raise forms.ValidationError(u"Error: passwords dont match. Try again.")
			else:
				pass
		return cd

def page(request):
	u = request.user
	if request.POST:
		if "cancel" in request.POST:
			return HttpResponseRedirect(reverse_lazy('index'))
		else:
			form = PasswordUpdateView(request.POST)
			if form.is_valid():
				#Se confirma al remitente el shipment, se avisa a cada admin y se guarda el message en la bbdd
				if u.is_active:
					u.set_password(raw_password=request.POST['password_uno'])
					u.save()
					messages.success(request, 'Ha cambiado your contraseña <b>correctly</b>.')
					#notificar !!
				return HttpResponseRedirect(reverse_lazy('panel'))
			else:
				return render(request, 'cambio_pass.html',{'form':form,'user':u})

	else:
		form=PasswordUpdateView()
		return render(request,'cambio_pass.html',{'form':form,'user':u})

	