# -*- coding: utf-8 -*-
#from secretSettings import *
from django.conf.urls import patterns, url, include
import os
import django

"""
General configurations of the project
"""

#django.settings()

SECRET_KEY = "blablablabla"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIRST_DAY_OF_WEEK = 1
CAPTCHA_FONT_SIZE = 30
CAPTCHA_OUTPUT_FORMAT = u'%(text_field)s %(image)s %(hidden_field)s'
CAPTCHA_LENGTH = 5
DEBUG = True
TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'theCode/templates')]
ALLOWED_HOSTS = ['*']

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages"
)

INSTALLED_APPS = (
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fsm_admin',  # administration of states of order
    'django_fsm', # Finite State Machine to manage orders
    'django_fsm_log',  # historical of orders
    'django_extensions',  # Tools to print graphics from the models, and the FSM
    'landing',
    'clients',
    'shop',
    'events',
    'contact_messages',
    'warehouse',
    'notifications',
    'graphos',
    'easy_pdf',  # pdf generation for invoice
    'bootstrap3',  # bootstrap for Django
    'captcha',  # test of touring
)

MIDDLEWARE_CLASSES = (

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

)

ROOT_URLCONF = 'theCode.urls'

WSGI_APPLICATION = 'theCode.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # TODO: postgreSQL
        'NAME': os.path.join(BASE_DIR, 'db3lite'),
    }
}
AUTH_USER_MODEL = 'clients.UserModel'

AUTHENTICATION_BACKENDS ={
    'theCode.customForms.backend.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
}
LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LANGUAGE_CODE = 'en-us'  # 'es-spa'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

MEDIA_URL = '/media/'
STATIC_URL = '/static/'  # url to use when asking for static files
MEDIA_ROOT = '/var/www/html/media/'  # where user uploads will go
STATIC_ROOT = "/var/www/html/static/"  # where collectstatic goes to search files for deployment

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
    )
# email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'unaaddress@gmail.com'
SERVER_EMAIL = 'unaaddress@gmail.com'
EMAIL_HOST_USER = 'unaaddress@gmail.com'
EMAIL_SUBJECT_PREFIX  = 'A name for the Web'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# graph models to print out Models relations
GRAPH_MODELS = {
   'all_applications': True,
   'group_models': True,
}
