# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.exceptions import ValidationError
from graphos.renderers import gchart
from graphos.sources.order import MooflDataSource
from proyecto.almacen.models import Product
#un pastel con los types actuales of cada product
#uno of barras con las number_of_visitis por dia of cada product
def page(request):
	try:
		lista_type = Product.objects.all()
	except Product.DoesNotExist:
		lista_type=[]
	chart= gchart.PieChart(MooflDataSource(lista_type, fields=["name", "number_of_visitis"]))
 	return render(request,'grafico_products.html',{'lista_type':lista_type,'chart':chart}) 

