# -*- coding: utf-8 -*-
from django.shortcuts import render
from theCode.shop.models import Sale

def page(request):
	lista_type = Sale.objects.all()
 	return render(request,'sales_charts.html',{'lista_type':lista_type}) 