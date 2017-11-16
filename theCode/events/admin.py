# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'begin_date', 'end_date', 'description')

    def clean(self):
        start_date = self.cleaned_data.get('begin_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("The end date can't be before begin date.")
        return self.cleaned_data



class EventAdmin(admin.ModelAdmin):
    form = EventForm
    list_display = ('name', 'begin_date', 'description')
    search_fields = ('name', 'description')

admin.site.register(Event, EventAdmin)
