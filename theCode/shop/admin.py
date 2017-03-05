# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Order,Shipment
from fsm_admin.mixins import FSMTransitionMixin # very cool FSM!!


class OrderAdmin(FSMTransitionMixin,admin.ModelAdmin):
    fields             = ('user','paid','module','information','special_coof','painting','sale','color')
    exclude         = ('sign_date',)
    list_display     = ('user','estado','paid','module','sign_date','sale')
    search_fields     = ('name', 'sign_date')
    readonly_fields = ('estado',)
    list_filter     = ('estado',)
    fsm_field         = ['estado',]


class ShipmentAdmin(admin.ModelAdmin):
    fields = ('number','shipment_price','order','date_received','additional_info','received','comp')
    exclude = ('sign_date',)
    list_display = ('number','sign_date','received','order','comp')
    search_fields = ('number','sign_date')


admin.site.register(Order,OrderAdmin)
admin.site.register(Shipment,ShipmentAdmin)