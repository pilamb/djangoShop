# -*- coding: utf-8 -*-

from django.shortcuts import render
from warehouse.models import Product


def page(request):
    list_type = Product.objects.filter(type='1')
    return render(request,
                  'warehouse/products.html',
                  {'list_type': list_type}
                  )
