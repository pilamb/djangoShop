# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from theCode.core.validators import *


class Event(models.Model):
    """
    Represents a simple event,
    something that the website wants to advert to users.
    """
    name = models.CharField(max_length=100,
                            verbose_name="Name:")
    begin_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True,
                                   verbose_name="Description:",
                                   max_length=1000)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.begin_date)

    def get_absolute_url(self):
        return reverse('event_list', kwargs={'pk': self.pk})

    class Meta:
        app_label = "events"
