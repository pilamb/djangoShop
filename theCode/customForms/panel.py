# -*- coding: utf-8 -*-

from datetime import date
from django.shortcuts import render
from clients.models import UserModel

from shop.models import Order, Sale, Shipment
from warehouse.models import Product
from messages_app.models import MessageModel, Alert


def page(request):
    if request.user.is_admin:
        try:
            object_list = UserModel.objects.exclude(
                is_admin=True).filter(is_superuser=False).\
                order_by('-sign_date')  # [:5]
        except UserModel.DoesNotExist:
            object_list = ()
        try:
            object_list2 = Order.objects.all()
        except Order.DoesNotExist:
            object_list2 = ()
        try:
            object_list3 = Sale.objects.all()
        except Sale.DoesNotExist:
            object_list3 = ()
        try:
            object_list4 = Shipment.objects.all()
        except Shipment.DoesNotExist:
            object_list4 = ()
        try:
            n_admins = Alert.objects.all().count()
        except Alert.DoesNotExist:
            n_admins = 0
        try:
            news = MessageModel.objects.filter(date=date.today()).count()
        except MessageModel.DoesNotExist:
            news = 0
        try:
            prods = Product.objects.all().count()
        except Product.DoesNotExist:
            prods = ()
    else:
        object_list = ()
        object_list2 = ()
        object_list3 = ()
        object_list4 = ()
        prods = ()
        n_admins = 0
        news = 0
        u = request.user
        n = MessageModel.objects.filter(user=u, notified=False).count()
        u.messages = n
        u.save()
    return render(request, 'user_panel.html', {
        'object_list': object_list,
        'object_list2': object_list2,
        'object_list3': object_list3,
        'object_list4': object_list4,
        'n_admins': n_admins,
        'news': news,
        'prods': prods
        }
    )
