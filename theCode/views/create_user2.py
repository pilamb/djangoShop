# -*- coding: utf-8 -*-

from django import forms
from django.shortcuts import render
from django.http 	import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from proyecto.clients.models import User_model
from captcha.fields import CaptchaField
from django.forms import RadioSelect
from django.contrib import messages
from django.contrib.auth.models import User
from proyecto.messages.models import Message
from proyecto.core.validador import only_letters,nums


class Form_Alta_User_model(forms.Form):

	required_css_class 	 = "required"
	error_css_class 	 = "notified-danger"
	email  	  = forms.EmailField(
		label="Email",
		help_notified='It will be used to log in.',
		max_length=50,
		widget= forms.TextInput(attrs={
			'class':'form-control',
			'placeholder':'Write an email',
			'onblur':'this.placeholder="Write an email"',
			'onclick':'this.placeholder=""',
			'type':'email'
			})
		)
	password  = forms.CharField(
		max_length=9,
		label="Password",
		widget = forms.PasswordInput(attrs={
			'class':'form-control',
			'placeholder':'Choose a password',
			'onblur':'this.placeholder="Choose a password"',
			'onclick':'this.placeholder=""',
			'type':'password'
			})
		)
	password2 = forms.CharField(
		max_length=9,
		required=False,
		label="Repeat",
		widget = forms.PasswordInput(attrs={
			'class':'form-control',
			'placeholder':'Repeat the password',
			'onblur':'this.placeholder="Repeat the password"',
			'onclick':'this.placeholder=""',
			'type':'password'
			})
		)
	name 	  = forms.CharField (max_length=20,
		label="Name",
		validators=[only_letters],
		widget= forms.TextInput (attrs={
			'class':'form-control',
			'placeholder':'Write a name of contact',
			'onblur':'this.placeholder="Write a name of contact"',
			'onclick':'this.placeholder=""'
			} 
	))
	surname = forms.CharField (max_length=40,
		label="Apellidos",
		validators=[only_letters],
		widget= forms.TextInput (attrs={
			'class':'form-control',
			'placeholder':'Write your surname',
			'onblur':'this.placeholder="Write your surname"',
			'onclick':'this.placeholder=""'
			} 
	))
	phone = forms.CharField(max_length=9,
		required=False,
		help_notified='Its not mandatory, only if you are willing to order.',
		label="Phone",
		validators=[nums],
		widget= forms.TextInput(attrs={
			'class':'form-control',
			'placeholder':'Phone',
			'onblur':'this.placeholder="A Phone"',
			'onclick':'this.placeholder=""',
			
			}
	))
	captcha   = CaptchaField()
	subscribed = forms.BooleanField(
		label="subscribed",
		required=False,
		help_notified='If you dont check this, you will NOT receive any mail from us.')
	acepto 	  = forms.BooleanField(label="Accept")

 	def clean_password2(self):
			pas = self.cleaned_data.get('password','')
			pas2 = self.cleaned_data.get('password2','')
			if not pas2 or not pas:
				raise forms.ValidationError("You must enter a password.")
			elif pas != pas2:
				raise forms.ValidationError("Passwords must match.")
			return pas

	def clean_acepto(self):
			a = self.cleaned_data.get('acepto')
			if not a:
				raise forms.ValidationError("It is mandatory to accept the conditions.")
			return a

def page(request):
	if request.POST: #si el form ha sido enviado, tratar los datos
		if "cancel" in request.POST:
			return HttpResponseRedirect(reverse_lazy('index'))
		else:
			form = Form_Alta_User_model(request.POST)
			if form.is_valid():#si el formulario es correcto, limpiar los campos
				name= form.cleaned_data['name']
				surname=form.cleaned_data['surname']
				email=form.cleaned_data['email']
				pas2 =form.cleaned_data['password2']
				tel=form.cleaned_data['phone']
				newUser_model=User_model(email=email,is_active=True,name=name,surname=surname,phone=tel, messages=1)
				newUser_model.set_password(pas2)
				newUser_model.save()
				notificacion_nueva = Message(user=newUser_model,notified=False,notified=u"Welcome to the website! You have an available account.")
				notificacion_nueva.save()
				messages.success(request, 'New user created correctly.')
				if request.user.is_anonymous:
					return HttpResponseRedirect(reverse_lazy('index'))
				else: 
					if request.user.is_admin:
						return HttpResponseRedirect(reverse_lazy('users_list'))
					else:
						return HttpResponseRedirect(reverse_lazy('panel'))			
			else:
				return render(request,'create_user.html',{'form':form})
	else:
		form=Form_Alta_User_model()
		return render(request,'create_user.html',{'form':form})
