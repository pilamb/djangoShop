# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.exceptions import ValidationError
from graphos.renderers import gchart
from graphos.sources.order import ModelDataSource
from theCode.warehouse.models import Product
#un pastel con los types actuales of cada product
#uno of barras con las number_of_visitis por dia of cada product
def page(request):
	try:
		list_type = Product.objects.all()
	except Product.DoesNotExist:
		list_type=[]
	chart= gchart.PieChart(ModelDataSource(list_type, fields=["name", "number_of_visitis"]))
 	return render(request,'products_charts.html',{'list_type':list_type,'chart':chart}) 

