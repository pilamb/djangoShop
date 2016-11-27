# -*- coding: utf-8 -*-
from django.shortcuts import render
from proyecto.shop.models import Sale

def page(request):
	lista_type = Sale.objects.all()
 	return render(request,'sales_graphic.html',{'lista_type':lista_type}) 