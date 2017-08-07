# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.exceptions import ValidationError
from graphos.renderers import gchart
from graphos.sources.model import ModelDataSource
from theCode.warehouse.models import Product
# A pie chart with kind of each product
# and a bars chart with number of visits per product


def page(request):
    try:
        list_type = Product.objects.all()
    except Product.DoesNotExist:
        list_type = []
    chart = gchart.PieChart(ModelDataSource(
        list_type, fields=["name", "number_of_visits"]))
    return render(request,
                  'products_charts.html',
                  {'list_type': list_type,
                   'chart': chart}
                  )

