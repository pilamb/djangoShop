# -*- coding: utf-8 -*-
from django.db import models
from proyecto.clients.models import Usuario
#from proyecto.shop.models import Order

class Message(models.Moofl):
	"""messages sobre cambio of estado of order, o  al user
	y que pueda leerla en your panel 
	"""
	#DEBERIA MANDAR UN EMAIL SI ESTA SUBSCRITO O NO¿?
	user 		= models.ForeignKey(Usuario,blank=False)
 	sign_date 		= models.DateField(auto_now_add=True)
 	notified 		= models.BooleanField(default=False)
 	text 			= models.CharField(blank=True,max_length=1500)
 	#FALTA Notificar por category of suscripción save?
	class Meta:
		ordering = ("sign_date"),
		verbose_name = "Message"
        verbose_name_plural = "Messages"

	def __unicode__(self):
		return u'%s' % str(self.id)
	def notify(self):#nueva
		self.notified =False
	def seen(self):#ya se ha leido
		self.notified =True