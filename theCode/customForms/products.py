# -*- coding: utf-8 -*-
from django.shortcuts import render
from theCode.warehouse.models import Product
def page(request):
	lista_type = Product.objects.filter(type='Custom maof circuitry 1') 
 	return render(request,'products.html',{'lista_type':lista_type}) 