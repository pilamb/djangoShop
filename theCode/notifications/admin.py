# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Notification


class NotificationAdminClass(admin.ModelAdmin):
    fields  = ('user', 'notified', 'notified')
    exclude = ('sign_date',)
    list_display = ('notified', 'user', 'sign_date', 'text')

admin.site.register(Notification, MessageClassAdmin)
