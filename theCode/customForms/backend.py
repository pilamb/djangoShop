# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import check_password
from proyecto.clients.models import User_model

class EmailAuthBackend(object):
    """
    Authenthicate backend based on email.
    """
    
    def authenticate(self, email=None, password=None):
        """
        Authentication method
        """
        try:
            user = User_model.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except User_model.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User_model.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User_model.DoesNotExist:
            return None