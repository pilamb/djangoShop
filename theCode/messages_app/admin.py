# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Message_class,Alert

def message_part(obj,length=10, suffix='...'):
    if len(unicode(obj.message)) <= length:
        return obj.message
    else:
        return ' '.join(obj.message[:length+1].split(' ')[0:-1]) + suffix
message_part.short_description = 'Notification'

class Message_classAdmin(admin.ModelAdmin):
    fields = ('attendedd','message')
    list_display = ('attended','name','mail','date',message_part,'is_member','category')
    search_fields = ('mail','date','category')
    
admin.site.register(Message_class,Message_classAdmin)
admin.site.register(Alert)
