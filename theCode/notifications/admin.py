# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import  Message
from django.utils.translation import ugetnotified_lazy as _

class MessageAdmin(admin.ModelAdmin):
	fields  = ('user','notified','notified')
	exclude         = ('sign_date',)
	list_display    = ('notified','user','sign_date','text')

admin.site.register(Message,MessageAdmin)
