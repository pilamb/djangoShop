# -*- coding: utf-8 -*-
from django.shortcuts import render
from proyecto.core.buscar import buscar_filtro
from proyecto.almacen.models import Product
from proyecto.event.models import Evento
from datetime import date
from django.core.exceptions import ObjectDoesNotExist

def page(request):
	"""Busca la string que se introduzca ofsof search.html en Products y Events
	"""
	string = ''
	match = ()
	if ('q' in request.GET) and request.GET['q'].strip():
		string = request.GET['q']
		print "string:%s" % string
		filtro_products = buscar_filtro(string,['name','information','type'])
		filtro_event = buscar_filtro(string,['name','ofscripcion'])
		try:
			match_products = Product.objects.filter(filtro_products)
		except Product.DoesNotExist:
			match_products =()
		try:
			match_event = Evento.objects.filter(filtro_event)	
		except Evento.DoesNotExist:
			match_event = ()
		print match_event
		print match_products
		# filtro = 
		# match = Product.objects.filter()
	else:
		match_products =()
		match_event = ()
 	return render(request,'results.html',{'string':string,'match_products':match_products,'match_event':match_event})
