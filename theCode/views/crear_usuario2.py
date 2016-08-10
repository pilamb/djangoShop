# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.http 	import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from proyecto.clients.models import Usuario
from captcha.fields import CaptchaField
from django.forms import RadioSelect
from django.contrib import messages
from django.contrib.auth.models import User
from proyecto.messages.models import Message
from proyecto.core.validador import letras,nums
#vista para la creación of users, validacion y diseño

class Form_Alta_Usuario(forms.Form):
	required_css_class 	 = "required"
	error_css_class 	 = "notified-danger"
	email  	  = forms.EmailField(
		label="Email",
		help_notified='Se usará para iniciar sesión, NO se pueof cambiar',
		max_length=50,
		widget= forms.TextInput(attrs={
			'class':'form-control',
			'placeholofr':'Write a email',
			'onblur':'this.placeholofr="Write a email"',
			'onclick':'this.placeholofr=""',
			'type':'email'
			})
		)
	password  = forms.CharField(
		max_length=9,
		label="Password",
		widget = forms.PasswordInput(attrs={
			'class':'form-control',
			'placeholofr':'Elija una contraseña',
			'onblur':'this.placeholofr="Elija una contraseña"',
			'onclick':'this.placeholofr=""',
			'type':'password'
			})
		)
	password2 = forms.CharField(
		max_length=9,
		required=False,
		label="Repita",
		widget = forms.PasswordInput(attrs={
			'class':'form-control',
			'placeholofr':'Repita la contraseña',
			'onblur':'this.placeholofr="Repita la contraseña"',
			'onclick':'this.placeholofr=""',
			'type':'password'
			})
		)
	name 	  = forms.CharField (max_length=20,
		label="Nombre",
		validators=[letras],
		widget= forms.TextInput (attrs={
			'class':'form-control',
			'placeholofr':'Write a name of contact',
			'onblur':'this.placeholofr="Write a name of contact"',
			'onclick':'this.placeholofr=""'
			} 
	))
	surname = forms.CharField (max_length=40,
		label="Apellidos",
		validators=[letras],
		widget= forms.TextInput (attrs={
			'class':'form-control',
			'placeholofr':'Write sus surname',
			'onblur':'this.placeholofr="Write sus surname"',
			'onclick':'this.placeholofr=""'
			} 
	))
	phone = forms.CharField(max_length=9,
		required=False,
		help_notified='No es obligatorio, solo si piensa realizar un order.',
		label="Teléfono",
		validators=[nums],
		widget= forms.TextInput(attrs={
			'class':'form-control',
			'placeholofr':'Un Teléfono',
			'onblur':'this.placeholofr="Un teléfono"',
			'onclick':'this.placeholofr=""',
			
			}
	))
	captcha   = CaptchaField()
	subscribed = forms.BooleanField(
		label="Sucripción",
		required=False,
		help_notified='Si no lo marca, no recibirá ningún correo nuestro en your email.')
	acepto 	  = forms.BooleanField(label="Acepto")
	#Falta definir las suscripciones a que
 	def clean_password2(self):
			pas = self.cleaned_data.get('password','')
			pas2 = self.cleaned_data.get('password2','')
			if not pas2 or not pas:
				raise forms.ValidationError("Debe introducir un password para confirmar.")
			elif pas != pas2:
				raise forms.ValidationError("Los passwords ofben ser idénticos.")
			return pas
	def clean_acepto(self):
			a = self.cleaned_data.get('acepto')
			if not a:
				raise forms.ValidationError("Es obligatorio aceptar las condiciones.")
			return a
	#Falta clean_email y mirar que no exista ya,controlando la excepción provocada
def page(request):
	if request.POST: #si el form ha sido enviado, tratar los datos
		if "cancel" in request.POST:
			return HttpResponseRedirect(reverse_lazy('index'))
		else:
			form = Form_Alta_Usuario(request.POST)
			if form.is_valid():#si el formulario es correcto, limpiar los campos
				name= form.cleaned_data['name']
				surname=form.cleaned_data['surname']
				email=form.cleaned_data['email']
				pas2 =form.cleaned_data['password2']
				tel=form.cleaned_data['phone']
				newUsuario=Usuario(email=email,is_active=True,name=name,surname=surname,phone=tel, messages=1)
				newUsuario.set_password(pas2)
				newUsuario.save()
				notificacion_nueva = Message(user=newUsuario,notified=False,notified=u"Bienvenido a la web of Turanga! Ya dispones of una cuenta of user.")
				notificacion_nueva.save()
				messages.success(request, 'Nuevo user creado correctly.')
				if request.user.is_anonymous:
					return HttpResponseRedirect(reverse_lazy('index'))
				else: 
					if request.user.is_admin:
						return HttpResponseRedirect(reverse_lazy('listado_users'))
					else:
						return HttpResponseRedirect(reverse_lazy('panel'))			
			else:
				return render(request,'crear_user.html',{'form':form})
	else:
		form=Form_Alta_Usuario()
		return render(request,'crear_user.html',{'form':form})
			
