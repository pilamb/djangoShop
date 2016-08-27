# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.exceptions import ValidationError
from proyecto.clients.models import Usuario
from proyecto.shop.models import Order,Sale,Shipment
from proyecto.messages.models import Message
from proyecto.almacen.models import Product
from proyecto.messages.models import Message, Alert
from datetime import date

def page(request):
	if request.user.is_admin:
		try:
			object_list = Usuario.objects.exclude(is_admin=True).filter(is_superuser=False).order_by('-sign_date')#[:5]
		except Usuario.DoesNotExist:
			object_list =()
		try:
			object_list2 = Order.objects.all()
		except Order.DoesNotExist:
			object_list2=()
		try:
			object_list3 = Sale.objects.all()
		except Sale.DoesNotExist:
			object_list3=()
		try:
			object_list4 = Shipment.objects.all()
		except Shipment.DoesNotExist:
			object_list4=()
		try:
			n_admins = Alert.objects.all().count()
		except Alert.DoesNotExist:
			n_admins=0
		try:
			news = Message.objects.filter(date=date.today()).count()
		except Message.DoesNotExist:
			news=0
		
		try:
			prods = Product.objects.all().count()
		except Product.DoesNotExist:
			prods =()
	else:
		object_list = ()
		object_list2 = ()
		object_list3 = ()
		object_list4 = ()
		prods =()
		n_admins=0
		news=0
		u = request.user
		n = Message.objects.filter(user = u,notified=False).count()
		u.messages = n 
		u.save()
 	return render(request,'panel_user.html',{'object_list':object_list,'object_list2':object_list2,'object_list3':object_list3,'object_list4':object_list4, 'n_admins':n_admins,'news':news,'prods':prods})
