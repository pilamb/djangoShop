# -*- coding: utf-8 -*-

from django.db import models
from proyecto.clients.models import Usuario


class Message(models.Model):
	"""
	Messages about change of state of an order, or about user account.
	Readable from user panel.
	"""

	user 		= models.ForeignKey(Usuario,blank=False)
 	sign_date	= models.DateField(auto_now_add=True)
 	notified 	= models.BooleanField(default=False)  # Changes when clicks on it
 	text 		= models.CharField(blank=True, max_length=1500)

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
