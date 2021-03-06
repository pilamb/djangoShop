# -*- coding: utf-8 -*-

from datetime import date
from django.shortcuts import render
from clients.models import UserModel

from shop.models import Order, Sale, Shipment
from warehouse.models import Product
from notifications.models import Notification
from contact_messages.models import  ContactMessage


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
            news = ContactMessage.objects.filter(date=date.today()).count()
        except ContactMessage.DoesNotExist:
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
        n_admins = 0  # TODO: this
        news = 0
        user = request.user
        nots = Notification.objects.filter(user=user, notified=False).count()
        # TODO: refactor this using related or some shit
        user.messages = nots
        user.save()
    return render(request, 'user_panel.html', {
        'object_list': object_list,
        'object_list2': object_list2,
        'object_list3': object_list3,
        'object_list4': object_list4,
        'n_admins': 0,
        'news': news,
        'prods': prods
        }
    )
