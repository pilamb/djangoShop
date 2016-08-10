# -*- coding: utf-8 -*-
from django.shortcuts import render
from proyecto.almacen.models import Product
def page(request):
	lista_type = Product.objects.filter(type='Custom maof circuitry 1') 
 	return render(request,'sirenas.html',{'lista_type':lista_type}) 