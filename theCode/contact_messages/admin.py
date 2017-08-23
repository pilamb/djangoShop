# -*- coding: utf-8 -*-

from django.contrib import admin
from models import ContactMessage, Alert


class ContactMessageModelAdmin(admin.ModelAdmin):
    def message_part(obj, length=10, suffix='...'):
        if len(unicode(obj.message)) <= length:
            return obj.message
        else:
            return ' '.join(obj.message[:length + 1].split(' ')[0:-1]) + suffix

    fields = ('attended', 'message')
    list_display = ('attended', 'name', 'mail', 'date', message_part,
                    'is_member', 'category')
    search_fields = ('mail', 'date', 'category')
    
admin.site.register(ContactMessage, ContactMessageModelAdmin)
admin.site.register(Alert)