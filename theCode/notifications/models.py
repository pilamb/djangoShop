# -*- coding: utf-8 -*-

from django.db import models
from clients.models import UserModel


class Notification(models.Model):
    """
    Messages sent to an user. Can be read at the user panel.
    Message_classs about change of state of an order, or about user account.
    Readable from user panel.
    """

    user = models.ForeignKey(UserModel,blank=False)
    sign_date = models.DateField(auto_now_add=True)
    notified = models.BooleanField(default=False)  # Changes when clicks on it
    text = models.CharField(blank=True, max_length=1500)

    class Meta:
        app_label = "notifications"
        ordering = "sign_date",
        verbose_name = "Notification"
        verbose_name_plural = "Notifications to users"

    def __unicode__(self):
        return u'%s' % str(self.id)

    def notify(self):  # a new message or event to say to user
        self.notified = False

    def seen(self):  # already read
        self.notified = True
