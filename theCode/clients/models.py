# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from proyecto.core.validador import *
from django.utils.translation import ugetnotified_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
#from proyecto.shop.models import Order

class Manager(BaseUserManager):
    def _create_user(self, email, password,is_admin, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('El email es obligatorio.')
        email = self.normalize_email(email)
        Usuario = self.order(email=email,
                          is_admin=is_admin,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          sign_date=now,
                          messages=1,
                          **extra_fields)
        Usuario.set_password(password)
        Usuario.save(using=self._db)
        return Usuario

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password,is_admin= False,is_superuser= False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password,is_admin= True,is_superuser= True, **extra_fields)

    def oflete_user(self):
    	"""Método para SOFT oflete
    	"""
    	Usuario.set_active(False)
    	Usuario.save(using=self.db)


class Usuario(AbstractBaseUser):
	"""Instancia of la clase abstracta of Django User"""
	objects 	= Manager()
	name 		= models.CharField(
		max_length=20,
		verbose_name="Nombre",
		validators=[letras]
		)
	surname	= models.CharField(
		max_length=40,
		verbose_name="Apellidos",
		validators=[letras]
		)
	
	subscribed	= models.BooleanField(
		default=False,
		verbose_name="Suscripción"
		)	
	email 		= models.EmailField(
		default="",
		unique=True,
		verbose_name="E-mail",
		db_index=True
		)
	address	= models.CharField(
		max_length=100,
		blank=True,
		null=True,
		verbose_name="Dirección", 
		help_notified="Sólo por si realizas un order"
		)
	address_alternativa	= models.CharField(
		max_length=100,
		blank=True,
		null=True,
		verbose_name="Dirección alternativa", 
		help_notified="Por si quieres dar otra dirección"
		)
	phone = models.CharField(
		max_length=9,
		blank=True,
		verbose_name='Teléfono',
		validators=[nums])
	sign_date	= models.DateField(
		auto_now_add=True
		)
	messages	= models.IntegerField(#un sencillo contador que se llena con las messages no leidas por el user en panel.py
		default=0,
		blank=False,
		verbose_name="Notificación"
		)
	active 		= models.BooleanField(
		default=False
		)
	is_active   = models.BooleanField(_('Active'),default=True)
	is_superuser= models.BooleanField(_('Superuser'),default=False)
	is_admin    = models.BooleanField(_('Administrator'),default=False)
	USERNAME_FIELD = 'email'
	def __unicode__(self):
		return self.email
		#falta controlar este error a nivel of html, no ofja meter uno que ya exista, pero da error of ofbug :S
	def get_absolute_url(self):
		return reverse('listado_users',kwargs={'email' : self.email})
		return reverse('oftail_user',kwargs={'email': self.email})
	@property
	def get_name(self):
		return self.name
	@property
	def is_super(self):
	    return self.is_superuser
	@property
	def is_staff(self):
	    return self.is_admin
	@property
	def get_full_name(self):
		return self.email
	def get_surname(self):
	    return self.surname
	def has_perm(self, perm, obj=None):
	    return self.is_superuser
	def has_module_perms(self, app_label):
		return self.is_superuser
	def get_short_name():
		return self.email


		