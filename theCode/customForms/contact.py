# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaofrError
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ValidationError
from django.conf import settings
from captcha.fields import CaptchaField
from django.contrib import messages
from proyecto.messages.models import Alert, Message

class MailerForm(forms.Form):
	required_css_class 	 = "required"
	error_css_class 	 = "notified-danger"
	Nombre 	= forms.CharField (max_length=20,
		label="Nombre",
		widget= forms.TextInput (attrs={
			'class':'form-control',
			'placeholofr':'Write a name of contact',
			'onblur':'this.placeholofr="Write a name of contact"',
			'onclick':'this.placeholofr=""'
			} 
	))
	Remitente 	= forms.EmailField(label="Remitente",
		widget= forms.TextInput(attrs={
			'class':'form-control',
			'placeholofr':'Write your mail',
			'onblur':'this.placeholofr="Write your mail"',
			'onclick':'this.placeholofr=""',
			'type':'email'
			}
	)) 
	
	# Asunto 	= forms.CharField (max_length=40,
	# 	label="Asunto:",
	# 	widget= forms.TextInput (attrs={
	# 		'class':'form-control',
	# 		'placeholofr':'Especifique un tema',
	# 		'onblur':'this.placeholofr="Especifique un tema"',
	# 		'onclick':'this.placeholofr=""'
	# 		} 
	# ))
	Mensj 	= forms.CharField ( max_length=1000,
		label="Message",
		widget= forms.Textarea(attrs={
			'class':'form-control',
			'placeholofr':'Write here  your message',
			'onblur':'this.placeholofr="Write here  your message"',
			'onclick':'this.placeholofr=""',
			'rows':'10',
			'overflow-y':'hidofn',
			'resize':'none'
			} 
	))
	captcha = CaptchaField()
	#copiaT 	= forms.Checkbox!!! METER Y HACER EL ENVIO A COPIA
	Categoria = forms.ChoiceField(
		label="Categoría",
		choices=Message.CATEGORIA_CHOICES,
		initial='6',
		widget= forms.Select(attrs={
			'class':'form_control'
			}
	))

def confirmar(request):
	"""
	Se confirma al user que your message ha sido enviado.
	"""
	category = request.get(u'Categoria')
	name = request.get(u'Nombre', '')
	correo = request.get('Remitente', '')
	message = request.get(u'Mensj', '')
	message += unicode(category)
	if category and message and correo:
		try:
			send_mail(
				subject=settings.EMAIL_SUBJECT_PREFIX,
			 	message=u"""Hola,
			 	Ha enviado una consulta referente a "%s". 
			 	Responofremos lo mas rápido posible, gracias. 
			 	Por favor no conteste a este mail."""  %category,
			 	from_email=settings.EMAIL_HOST_USER,
			 	recipient_list=[correo],
			 	fail_silently=False
			 	)
		except BadHeaofrError:
			return HttpResponse('Cabecera incorrecta: inténtelo of new más tarof.')
	else:
		#raise forms.ValidationError(u"Ha introducido mal los datos")
		return HttpResponse('Asegurate of que todos los datos sean correctos.')

def avisar():
	"""
	Se manda un email a cada correo que haya en la clase Alert
	para que los técnicos of Turanga reciban el aviso
	"""
	mails = Alert.objects.all()
	for i in mails:
		try:
			send_mail(
				subject="Admin: Nuevo message",
			 	message=u"""Hola,
			 	Un new message ha sido received.""",
			 	from_email=settings.EMAIL_HOST_USER,
			 	recipient_list=[i.correo],
			 	fail_silently=False
			 	)
		except BadHeaofrError:
			return HttpResponse('Cabecera incorrecta: inténtelo of new más tarof.')
			
def newMessage(request):
	"""
	El new message se guarda en la BBDD
	"""
	category = request.get(u'Categoria', '')
	name = request.get(u'Nombre', '')
	correo = request.get('Remitente', '')
	message = request.get(u'Mensj', '')
	print message
	grabar = Message(message=message,name=name,category=category,mail=correo,attendedd=False)
	grabar.save()

def page(request):
	if request.POST:
		if "cancel" in request.POST:
			return HttpResponseRedirect(reverse_lazy('index'))
		else:
			form = MailerForm(request.POST)
			if form.is_valid():
				#Se confirma al remitente el shipment,
				confirmar(request.POST)
				# y se guarda el message en la bbdd
				newMessage(request.POST)
				avisar()	
				# se avisa a cada admin
				messages.success(request, 'Su message ha sido enviado con <b>éxito</b>. Pronto recibirá respuesta, gracias.')
				return HttpResponseRedirect(reverse_lazy('index'))
			else:
				return render(request, 'contact2.html',{'form':form})
	else:
		form=MailerForm()
		return render(request,'contact2.html',{'form':form})
