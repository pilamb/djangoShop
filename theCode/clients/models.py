# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,\
    PermissionsMixin,\
    BaseUserManager
from django.utils import timezone
from theCode.core.validators import nums, only_letters


class Manager(BaseUserManager):
    def _create_user(
            self, email, password, is_admin, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The email is mandatory.')
        email = self.normalize_email(email)
        user = UserModel(email=email,
                         is_admin=is_admin,
                         is_active=True,
                         is_superuser=is_superuser,
                         last_login=now,
                         sign_date=now,
                         messages=1,
                         **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password,
                                 is_admin=False,
                                 is_superuser=False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password,
                                 is_admin=True,
                                 is_superuser=True,
                                 **extra_fields)

    def delete_user(self):
        self.set_active(False)
        self.save(using=self.db)


class UserModel(AbstractBaseUser):
    """
    Django User abstract heritage
    """

    objects = Manager()
    name = models.CharField(
        max_length=20,
        verbose_name="Name",
        validators=[only_letters]
        )
    surname = models.CharField(
        max_length=40,
        verbose_name="Surname",
        validators=[only_letters]
        )

    subscribed = models.BooleanField(
        default=False,
        verbose_name="Subscribed"
    )
    email = models.EmailField(
        default="",
        unique=True,
        verbose_name="E-mail",
        db_index=True
        )
    address = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Address",
        #help_notified="Only if you order, for delivery."
        )
    address_alternativa = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Second address ",
        #help_notified="Only if you order, for delivery."
        )
    phone = models.CharField(
        max_length=9,
        blank=True,
        verbose_name='Phone',
        validators=[nums])
    sign_date = models.DateField(
        auto_now_add=True
        )
    # a simple counter with unread messages for panel.py
    messages = models.IntegerField(
        default=0,
        blank=False,
        verbose_name="Message_classs"
        )
    active = models.BooleanField(
        default=False
        )
    is_active = models.BooleanField(_('Active'), default=True)
    is_superuser = models.BooleanField(_('Superuser'), default=False)
    is_admin = models.BooleanField(_('Administrator'), default=False)
    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('list_users', kwargs={'email': self.email})
        #return reverse('detail_user', kwargs={'email': self.email})

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

    def get_short_name(self):
        return self.email