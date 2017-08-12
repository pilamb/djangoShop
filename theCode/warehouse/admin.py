# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Product, Piece


class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'type_info', 'price', 'on_sale', 'information', 'picture',
              'url_sample', 'recipe')
    list_display = ('name', 'sign_date', 'type_info', 'price', 'on_sale',
                    'visits_number')
    # def save_order(self, request, obj, form, change):
    #     for i in request.POST.getlist('recipe'):
    #         print i
    #search_fields = ('mail','date','asunto')
    #readonly_fields = ('image_tag',)


class PieceAdmin(admin.ModelAdmin):    
    fields = ('name', 'quantity', 'value', 'unit', 'price', 'the_type',
              'provider', 'picture', 'note')
    list_display = ('name', 'quantity', 'value', 'unit', 'price', 'the_type',
                    'alarm')
    
admin.site.register(Piece, PieceAdmin)
admin.site.register(Product, ProductAdmin)
