# -*- coding: utf-8 -*-
from django.shortcuts import render


def page(request):
    return render(
         request,
         'shipments_info.html'
    )
