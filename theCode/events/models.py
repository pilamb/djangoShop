# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from proyecto.core.validador import *


class Event(models.Model):
	"""
    Represents a simple event, something that the website wants to advert to users.
    """

	name 		= models.CharField(max_length=20, verbose_name="Name:", validators=[only_letters])
	date		= models.DateField(auto_now=True, auto_now_add=True)
	description = models.CharField(blank=True, verbose_name="Description:", max_length=1000)

	def __unicode__(self):
		return u'%s%s' % (self.name,self.date)

	def get_absolute_url(self):
		return reverse('listado_user', kwargs={'pk' : self.pk})
		return reverse('detail_user', kwargs={'email': self.date})

