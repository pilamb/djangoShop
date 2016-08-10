# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.forms import Textarea, TextInput, PasswordInput, EmailInput
from django.contrib import messages
from proyecto.shop.models import Order
from proyecto.almacen.models import Product
from proyecto.messages.models import Message
#Reserva of un modulo ya escogido en un link
class Formulario_alta_Order_Concreto(forms.Form):
	def __init__(self,*args,**kwargs):
			self.request = kwargs.pop('request', None)
			super(Formulario_alta_Order_Concreto,self).__init__(*args,**kwargs)
	required_css_class 	 = "required"
	error_css_class 	 = "notified-danger"
	captcha = CaptchaField()
	
	notified 	= forms.CharField ( 
		max_length=1000,
		required=False,
		label="Message",
		widget= forms.Textarea(attrs={
			'class':'form-control',
			'placeholofr':'Write here  un message opcional',
			'onblur':'this.placeholofr="Write here  un message opcional"',
			'onclick':'this.placeholofr=""',
			'rows':'10',
			'overflow-y':'hidofn',
			'resize':'none'
			})
		)
	color = forms.ChoiceField(
		widget=forms.Select(attrs={
			'class':'form-control',
			'id':'selectorcolor',
			'onchange':'cambiaPrecio(this)',

			}),
		choices=Order.COLORES_CHOICES
		)
	class Meta:
		order = Order
		fields = ('user','information','paid','color')
		excluof = 'modulo'
	def clean(self):
		cleaned_data = super(Formulario_alta_Order_Concreto,self).clean()
		return cleaned_data

def page(request,pk):
	try:
		mod = Product.objects.get(id = pk)
	except Panel.DoesNotExist:
		mod = None
	print mod
	user = request.user
	if request.POST: #si el form ha sido enviado, tratar los datos
		if "cancel" in request.POST:
			return HttpResponseRedirect(reverse_lazy('index'))
		else:
			form = Formulario_alta_Order_Concreto(request.POST)
			if request.user.is_authenticated():

				if form.is_valid():
					notified = request.POST['notified']
					print request.POST['color']
					p = Order(
						user = user,
						modulo = mod,
						information = notified,
						paid = False,
						color = request.POST['color']
						)
					if mod.on_sale:
						mod.on_sale=False
						mod.save()
					if request.POST['color']!="Sin":
						p.pintura=True
					else:
						p.pintura=False
					p.save()
					notificacion_nueva = Message(user=user,notified=False,notified=u"Enhorabuena, el order ID %s se ha creado correctly y se encuentra en estado %s. Pronto recibirás confirmación of cambio of estado. Gracias" % (str(p.id),p.estado))
					notificacion_nueva.save()
					mod.quitar_of_sale()
					mod.save()
					messages.success(request, '¡Order creado <b>correctly</b>, gracias!')
					return HttpResponseRedirect(reverse_lazy('panel'))
				else:
					return render(request, 'crear_order.html',{'form':form,'pk':pk})
	else:
		form = Formulario_alta_Order_Concreto()
		return render(request,'crear_order.html',{'form':form,'pk':pk})
				

