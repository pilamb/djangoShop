# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import check_password
from clients.models import UserModel


class EmailAuthBackend(object):
    """
    Authenticate backend based on email.
    """
    
    def authenticate(self, email=None, password=None):
        """
        Authentication method
        """
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
            # TODO:  this is needs work
        except UserModel.DoesNotExist:
            return None
