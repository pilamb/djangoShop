# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from theCode.core.validators import *
from clients. models import UserModel


class MessageModel(models.Model):
    """
    When somebody writes at contact.py creates an instance of this type
    with attended to False and alerts are sent to admins
    """
    CATEGORY = (
        ('Orders', 'Orders'),
        ('Account', 'Account'),
        ('Products', 'Products'),
        ('Warranty', 'Warranty'),
        ('Events', 'Events'),
        ('Shipping', 'Shipping'),
        ('Others', 'Others'),
    )
    name = models.CharField(max_length=20,validators=[only_letters])
    date = models.DateField(auto_now_add=True)
    mail = models.EmailField()
    message = models.CharField(blank=True, max_length=1000)
    category = models.CharField(max_length=10,
                                choices=CATEGORY,
                                default='Others',
                                blank=False)
    attended = models.BooleanField(default=False,
                                   verbose_name="An admins has seen it.")

    def is_member(self):
        return UserModel.objects.filter(email=self.mail).exists()

    def __unicode__(self):
        return u'%s%s%s' % (self.name, str(self.date), self.mail)

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'email': self.date})

    class Meta:
        app_label = "messages_app"
        get_latest_by = "date"


class Alert(models.Model):
    """
    Admins emails to alert abount new events related to the website
    """
    mail = models.EmailField(unique=True,
                             help_text='Add email addresses to send alerts.')

    def __unicode__(self):
        return self.mail

    class Meta:
        verbose_name_plural = 'Alerts'
