# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Evento
class EventoAdmin(admin.MooflAdmin):
	fields = ('name','ofscripcion')
	list_display = ('name','date','ofscripcion')
	search_fields = ('name','ofscripcion')
	
admin.site.register(Evento,EventoAdmin)
