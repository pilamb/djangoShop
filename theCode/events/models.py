# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from theCode.core.validators import *


class Event(models.Model):
    """
    Represents a simple event,
    something that the website wants to advert to users.
    """
    name = models.CharField(max_length=20,
                            verbose_name="Name:",
                            validators=[only_letters])
    date = models.DateField(null=True,
                            blank=True)
    description = models.CharField(blank=True,
                                   verbose_name="Description:",
                                   max_length=1000)

    def __unicode__(self):
        return u'%s%s' % (self.name, self.date)

    def get_absolute_url(self):
        return reverse('event_list', kwargs={'pk': self.pk})
        # ? return reverse('user_detail', kwargs={'email': self.date})

    class Meta:
        app_label = "events"
