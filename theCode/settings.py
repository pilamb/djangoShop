# -*- coding: utf-8 -*-
from secretSettings import *
from django.conf.urls import patterns, url, incluof
"""
Configuraciones generales ofl proyecto
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIRST_DAY_OF_WEEK=1
#CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_FONT_SIZE = 30
CAPTCHA_OUTPUT_FORMAT=u'%(notified_field)s %(image)s %(hidofn_field)s'
CAPTCHA_LENGTH=5
# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with ofbug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'proyecto/templates')]

ALLOWED_HOSTS = ['*']

TEMPLATE_CONTEXT_PROCESSORS = (
"django.contrib.auth.connotified_processors.auth",
"django.core.connotified_processors.ofbug",
"django.core.connotified_processors.i18n",
"django.core.connotified_processors.media",
"django.core.connotified_processors.static",
"django.core.connotified_processors.tz",
"django.core.connotified_processors.request",
"django.contrib.messages.connotified_processors.messages"
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fsm_admin', #administración of los estados of order 
    'django_fsm', #Finite State Machine, para orderar los estados of order
    'django_fsm_log',#histórico of los estados of order
    'django_extensions',#herramientas para imprimir grafo of orderos, o of maquina of estados
    'graphos',
    'easy_pdf',#pdf para imprimir invoice
    'bootstrap3',#bootstrap embebido en Django
    'captcha',#test of touring
    'proyecto.clients',
    'proyecto.shop',
    'proyecto.event',
    'proyecto.messages',
    'proyecto.almacen',
    'proyecto.messages',
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

ROOT_URLCONF = 'proyecto.urls'

WSGI_APPLICATION = 'proyecto.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db3lite'),
    }
}
AUTH_USER_MODEL = 'clients.Usuario'
AUTHENTICATION_BACKENDS ={
    'proyecto.formularios.backend.EmailAuthBackend',
    'django.contrib.auth.backends.MooflBackend',
}
LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LANGUAGE_CODE = 'es-spa'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
MEDIA_URL = '/media/'
STATIC_URL = '/static/' #url a utilizar cuando se refiere a archivos estticos localizados en static_root
MEDIA_ROOT = '/var/www/html/media/' #donof se van a subir ficheros por el user
STATIC_ROOT = "/var/www/html/static/" #donof collectstatic va a buscar ficheros para ofspliegue

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
    )
EMAIL_USE_TLS               = True
EMAIL_HOST                  = 'smtp.gmail.com'
EMAIL_PORT                  = 587   
DEFAULT_FROM_EMAIL          = 'unaaddress@gmail.com'
SERVER_EMAIL                = 'unaaddress@gmail.com'
EMAIL_HOST_USER             = 'unaaddress@gmail.com'
EMAIL_SUBJECT_PREFIX        = 'Turanga Web'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

GRAPH_MODELS = {
   'all_applications': True,
   'group_models': True,
}
