# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

letras  = RegexValidator(r'^[A-ZÁÉÍÓÚÑÇÄËÏÖÜa-zñáéíóúäëïöüç\s]*$', 'Only letters allowed.')
nums	= RegexValidator(r'^[0-9]*$', 'Only numbers allowed.')
alfan	= RegexValidator(r'^[A-ZÁÉÍÓÚÑÇÄËÏÖÜa-zñáéíóúäëïöüç\,.-s0-9]*$', 'Only numbers and/or letters are allowed.')

def price_positivo(value):
	""" 
    0 is allowd for possibles defers in future
	"""
	if value<0:
		msg = u"Price must be over or = 0"
		raise ValidationError(msg)