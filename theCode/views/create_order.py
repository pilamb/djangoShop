#DO NOT USE ////////////////////////////

# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.forms import Textarea, TextInput, PasswordInput, EmailInput,RadioSelect
from django.contrib import messages
from theCode.shop.models import Order
from theCode.warehouse.models import Product
from theCode.messages_app.models import Message_class


class New_product_order_form(forms.Form):
	def __init__(self,*args,**kwargs):
			self.request = kwargs.pop('request', None)
			super(New_product_order_form,self).__init__(*args,**kwargs)
	required_css_class 	 = "required"
	error_css_class 	 = "notified-danger"
	captcha 			 = CaptchaField()
	product  = forms.ModelChoiceField(
			widget=forms.RadioSelect(attrs={
				'class':'radio',
			}),
			queryset=Product.objects.filter(on_sale=True),
			initial=1,
			)
	notified 	= forms.CharField ( 
		max_length=1000,
		required=False,
		label="Message_class",
		widget= forms.Textarea(attrs={
			'class':'form-control',
			'placeholder':'Write here an optional message',
			'onblur':'this.placeholder="Write here an optional message"',
			'onclick':'this.placeholder=""',
			'rows':'10',
			'overflow-y':'hidden',
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
		fields = ('user','product','information','colour')

	def clean(self):
		cleaned_data = super(New_product_order_form,self).clean()
		return cleaned_data

def page(request):
	user = request.user
	if request.POST: #si el form ha sido enviado, tratar los datos
		if "cancel" in request.POST:
			return HttpResponseRedirect(reverse_lazy('index'))
		else:
			form = New_product_order_form(request.POST)
			if request.user.is_authenticated():
				if form.is_valid():
					product = request.POST['product']
					mod = Product.objects.get(id = product)
					notified = request.POST['notified']
					painting = request.POST['color']
					print "You has choosen %s" % str(painting)
					print painting
					p = Order(
						user = user,
						product = mod,
						information = notified,
						paid = False,
						)
					mod.quitar_of_sale()
					mod.save()
					new_message = Message_class(user=user, notified=False, notified=u"""Congratulations, the order has been created correctly and it is in the state %s.
					 Soon you will receive confirmation of the states changes. Thanks""" % p.state)
					new_message.save()
					messages.success(request, '¡Order created <b>correctly</b>, thanks!')
					return HttpResponseRedirect(reverse_lazy('panel'))
				else:
					return render(request, 'create_order.html',{'form':form})
	else:
		form = New_product_order_form()
		return render(request,'create_order.html',{'form':form})
				
