# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import check_password
from proyecto.clients.models import Usuario

class EmailAuthBackend(object):
    """
    Authenthicate backend based on email.
    """
    
    def authenticate(self, email=None, password=None):
        """
        Authentication method
        """
        try:
            user = Usuario.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Usuario.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except Usuario.DoesNotExist:
            return None