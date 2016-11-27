# -*- coding: utf-8 -*-
from django.shortcuts import render
from proyecto.core.searcher import search_filter
from proyecto.almacen.models import Product
from proyecto.event.models import Event
from datetime import date
from django.core.exceptions import ObjectDoesNotExist

def page(request):
	"""Search for string on Products y Events
	"""
	search_string = ''
	match = ()
	if ('q' in request.GET) and request.GET['q'].strip():
		search_string = request.GET['q']
		products_filter = search_filter(search_string,['name','information','type'])
		event_filter = search_filter(search_string,['name','description'])
		try:
			match_products = Product.objects.filter(products_filter)
		except Product.DoesNotExist:
			match_products =()
		try:
			match_event = Event.objects.filter(event_filter)	
		except Event.DoesNotExist:
			match_event = ()
		# filtro = 
		# match = Product.objects.filter()
	else:
		match_products =()
		match_event = ()
 	return render(request,'results.html',{'search_string':search_string,'match_products':match_products,'match_event':match_event})
