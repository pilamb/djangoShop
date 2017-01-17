# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from proyecto.core.validador import *
from proyecto.clients. models import User_model

class Message(models.Model):
	"""
	When somebody writes at contact.py creates an instance of this type
	with attendedd to False and alerts are sent to admins
	"""
	CATEGORIA_CHOICES = (
		('Orders','Orders'),
		('Account','Account'),
		('Products','Products'),
		('Warranty' ,'Warranty'),
		('Events','Events'),
		('Shippings','Shippings'),
		('Others','Others'),				
	)
	name 		= models.CharField(max_length=20,validators=[only_letters])
	date		= models.DateField(auto_now=True,auto_now_add=True)
	mail 		= models.EmailField()
	message 	= models.CharField(blank=True, max_length=1000)
	category 	= models.CharField(max_length=10,choices=CATEGORIA_CHOICES,default='Others',blank=False)
	attendedd 	= models.BooleanField(default=False)
	def es_miembro(self):
		return User_model.objects.filter(email=self.mail).exists()
	def __unicode__(self):
		return u'%s%s%s' % (self.name, str(self.date), self.mail)
	def get_absolute_url(self):
		return reverse('listado_user',kwargs={'pk' : self.pk})
		return reverse('detail_user',kwargs={'email': self.date})
	class Meta:
		get_latest_by = "date"

class Alert(models.Model):
	""" 
	Admins emails to alert abount new events related to the website
	"""
	mail 		= models.EmailField(unique=True,help_text='Add email addresses to send alerts.')
	def __unicode__(self):
		return self.mail
	class Meta:
		verbose_name='Alert'
		verbose_name_plural='Alerts'
