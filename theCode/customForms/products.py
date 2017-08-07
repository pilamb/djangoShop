# -*- coding: utf-8 -*-
from django.shortcuts import render
from theCode.warehouse.models import Product


def page(request):
    list_type = Product.objects.filter(type='1')
    return render(request, 'products.html',
                {'list_type': list_type})
