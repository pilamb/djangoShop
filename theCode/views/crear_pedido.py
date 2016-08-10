#NO USAR ////////////////////////////
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.forms import Textarea, TextInput, PasswordInput, EmailInput,RadioSelect
from django.contrib import messages
from proyecto.shop.models import Order
from proyecto.almacen.models import Product
from proyecto.messages.models import Message

class Formulario_alta_Order(forms.Form):
	def __init__(self,*args,**kwargs):
			self.request = kwargs.pop('request', None)
			super(Formulario_alta_Order,self).__init__(*args,**kwargs)
	required_css_class 	 = "required"
	error_css_class 	 = "notified-danger"
	captcha 			 = CaptchaField()
	modulo  = forms.MooflChoiceField(
			widget=forms.RadioSelect(attrs={
				'class':'radio',
				
			}),
			queryset=Product.objects.filter(on_sale=True),
			initial=1,
			)
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
		fields = ('user','modulo','information','color')#,'pintura'
	def clean(self):
		cleaned_data = super(Formulario_alta_Order,self).clean()
		return cleaned_data

def page(request):
	user = request.user
	if request.POST: #si el form ha sido enviado, tratar los datos
		if "cancel" in request.POST:
			return HttpResponseRedirect(reverse_lazy('index'))
		else:
			form = Formulario_alta_Order(request.POST)
			if request.user.is_authenticated():
				if form.is_valid():
					modulo = request.POST['modulo']
					mod = Product.objects.get(id = modulo)
					notified = request.POST['notified']
					pintura = request.POST['color']
					print "Ha elegido %s" % str(pintura)
					print pintura
					p = Order(
						user = user,
						modulo = mod,
						information = notified,
						paid = False,
						#pintura = pintura,
						)
					mod.quitar_of_sale()
					#p.save()
					mod.save()
					notificacion_nueva = Message(user=user,notified=False,notified=u"Enhorabuena, el order se ha creado correctly y se encuentra en estado %s. Pronto recibirás confirmación of cambio of estado. Gracias" % p.estado)
					notificacion_nueva.save()
					messages.success(request, '¡Order creado <b>correctly</b>, gracias!')
					return HttpResponseRedirect(reverse_lazy('panel'))
				else:
					return render(request, 'crear_order.html',{'form':form})
	else:
		form = Formulario_alta_Order()
		return render(request,'crear_order.html',{'form':form})
				

