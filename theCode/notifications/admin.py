# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import  Message_class
from django.utils.translation import ugetnotified_lazy as _

class Message_classAdmin(admin.ModelAdmin):
	fields  = ('user','notified','notified')
	exclude         = ('sign_date',)
	list_display    = ('notified','user','sign_date','text')

admin.site.register(Message_class,Message_classAdmin)
