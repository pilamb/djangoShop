# -*- coding: utf-8 -*-
from django.shortcuts import render
from theCode.shop.models import Sale


def page(request):
    list_type = Sale.objects.all()
    return render(
        request,
        'sales_charts.html',
        {'list_type': list_type}
    )
