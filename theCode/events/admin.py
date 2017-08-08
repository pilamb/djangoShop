# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Event


class EventAdmin(admin.ModelAdmin):
    
    fields = ('name', 'description')
    list_display = ('name', 'date', 'description')
    search_fields = ('name', 'description')
    
admin.site.register(Event, EventAdmin)
