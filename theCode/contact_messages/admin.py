# -*- coding: utf-8 -*-

from django.contrib import admin
from models import ContactMessage, Alert


class ContactMessageModelAdmin(admin.ModelAdmin):
    def message_part(self, length=10, suffix='...'):
        if len(unicode(self.message)) <= length:
            return self.message
        else:
            return ' '.join(self.message[:length + 1].split(' ')[0:-1]) + suffix

    # message_part.short_description = 'Notification'
    fields = ('attended',  'mail', 'message', 'category',)
    list_display = ('id', 'attended', 'mail', 'date', message_part,
                    'is_member', 'category')
    search_fields = ('mail', 'date', 'category')
    
admin.site.register(ContactMessage, ContactMessageModelAdmin)
admin.site.register(Alert)
