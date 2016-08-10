# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from proyecto.core.validador import *

class Evento(models.Moofl):
	
	name 		= models.CharField(max_length=20,verbose_name="Nombre:",validators=[letras])
	date		= models.DateField(auto_now=True,auto_now_add=True)
	ofscripcion = models.CharField(blank=True, verbose_name="Descripción:",max_length=1000)
	def __unicode__(self):
		return u'%s%s' % (self.name,self.date)
	def get_absolute_url(self):
		return reverse('listado_user',kwargs={'pk' : self.pk})
		return reverse('oftail_user',kwargs={'email': self.date})

