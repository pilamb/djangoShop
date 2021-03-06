# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Order,Shipment
from fsm_admin.mixins import FSMTransitionMixin # very cool FSM!!


class OrderAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = ('user', 'paid', 'module', 'information', 'payment_code', 'sale')
    exclude = ('sign_date',)
    list_display = ('user', 'state', 'paid', 'module', 'sign_date', 'sale')
    search_fields = ('name', 'sign_date')
    readonly_fields = ('state',)
    list_filter = ('state',)
    fsm_field = ['state', ]


class ShipmentAdmin(admin.ModelAdmin):
    fields = ('tracking_number',
              'shipment_price',
              'order', 'date_received', 'additional_info', 'received', 'comp')
    exclude = ('sign_date',)
    list_display = ('tracking_number', 'sign_date', 'received', 'order', 'comp')
    search_fields = ('tracking_number', 'sign_date')


admin.site.register(Order, OrderAdmin)
admin.site.register(Shipment, ShipmentAdmin)
