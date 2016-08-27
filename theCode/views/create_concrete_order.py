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


class New_concret_product_order_form(forms.Form):
	def __init__(self,*args,**kwargs):
			self.request = kwargs.pop('request', None)
			super(New_concret_product_order_form,self).__init__(*args,**kwargs)

	required_css_class 	 = "required"
	error_css_class 	 = "notified-danger"
	captcha = CaptchaField()
	
	notified 	= forms.CharField ( 
		max_length=1000,
		required=False,
		label="Message",
		widget= forms.Textarea(attrs={
			'class':'form-control',
			'placeholder':'Write here an optional message',
			'onblur':'this.placeholder="Write here an optional message"',
			'onclick':'this.placeholder=""',
			'rows':'10',
			'overflow-y':'hidofn',
			'resize':'none'
			})
		)
	color = forms.ChoiceField(
		widget=forms.Select(attrs={
			'class':'form-control',
			'id':'selectorcolor',
			'onchange':'changePrice(this)',

			}),
		choices=Order.COLORES_CHOICES
		)
	class Meta:
		order = Order
		fields = ('user','information','paid','color')
<<<<<<< 9d91132817820e448c9812923042b09ec7571c60:theCode/views/create_concrete_order.py
		exclude = 'modulo'
=======
		exclude = ''
>>>>>>> more English translating:theCode/views/create_concrete_order.py
	def clean(self):
		cleaned_data = super(New_concret_product_order_form,self).clean()
		return cleaned_data

def page(request,pk):
	try:
		mod = Product.objects.get(id = pk)
	except Panel.DoesNotExist:
		mod = None
	print mod
	user = request.user
	if request.POST:
		if "cancel" in request.POST:
			return HttpResponseRedirect(reverse_lazy('index'))
		else:
			form = New_concret_product_order_form(request.POST)
			if request.user.is_authenticated():

				if form.is_valid():
					notified = request.POST['notified']
					print request.POST['color']
					p = Order(
						user = user,
						product = mod,
						information = notified,
						paid = False,
						color = request.POST['color']
						)
					if mod.on_sale:
						mod.on_sale=False
						mod.save()
					if request.POST['color']!="Sin":
						p.painting=True
					else:
						p.painting=False
					p.save()
					new_message = Message(user=user, notified=False, notified=u"""Congratulations, the order has been created correctly and it is in the state %s.
					 Soon you will receive confirmation of the states changes. Thanks""" % p.state)
					new_message.save()
					mod.quitar_of_sale()
					mod.save()
					messages.success(request, '¡Order created <b>correctly</b>, thanks!')
					return HttpResponseRedirect(reverse_lazy('panel'))
				else:
					return render(request, 'create_order.html',{'form':form,'pk':pk})
	else:
		form = New_concret_product_order_form()
		return render(request,'create_order.html',{'form':form,'pk':pk})
				

