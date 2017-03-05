# -*- coding: utf-8 -*-

from django.db import models
from theCode.clients.models import User_model


class Message_class(models.Model):
    """
    Message_classs about change of state of an order, or about user account.
    Readable from user panel.
    """

    user  = models.ForeignKey(User_model,blank=False)
    sign_date = models.DateField(auto_now_add=True)
    notified = models.BooleanField(default=False)  # Changes when clicks on it
    text = models.CharField(blank=True, max_length=1500)

    class Meta:
        ordering = ("sign_date"),
        verbose_name = "Message_class"
        verbose_name_plural = "Message_classs"

    def __unicode__(self):
        return u'%s' % str(self.id)

    def notify(self): # a new message or event to say to user
        self.notified =False

    def seen(self): # already read
        self.notified =True
