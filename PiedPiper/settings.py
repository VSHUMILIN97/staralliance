"""
Django settings for PiedPiper project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import django
from django.utils.translation import gettext_lazy as _
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tm3d(#yvvm^dz3*l908)w_#_!1r&f!5!5ep^rq@ghc*+rojo7u'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
COMPRESS_ENABLED = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.2.140',
    'arbitr.tenguai.com',
    '216.189.157.83',
    'vadim.sysnursery.org',
    'staralliance.pro',
    'www.staralliance.pro',
]

STARALLIANS_HOST = '216.189.157.83'
REDIS_DEFAULT_PORT = 6379
LOCAL_SERVICE_HOST = '127.0.0.1'
MONGODB_DEFAULT_PORT = 27017

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
STATICFILES_DIRS = (
        #'c:/users/pc/pycharmprojects/djangopiper/static', #
)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Exchanges',
    'rest_framework',
    'requests',
    'compressor',
    'bootstrap4',
    'jquery',
    'registration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PiedPiper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR + '/Exchanges/Templates/' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PiedPiper.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
"""DATABASES = {
    'default': {
        'ENGINE': '',
    },
}"""

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "Exchanges.routing.channel_routing",
    },
}
# Before

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'zTrash/db.sqlite3'),
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine',
        'NAME': 'PiedPiperStock',
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
    ('ru', _('Russian')),
    ('ar', _('Arab')),
    ('uk', _('Ukrainian')),
    ('fr', _('French'))
]

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = 'static'  # пустая папка, сюда будет собирать статику collectstatic

STATIC_URL = '/static/'  # URL для шаблонов

STATICFILES_DIRS = ('/Exchanges/Templates/', )


#REGISTRATION SETTINGS

ACCOUNT_ACTIVATION_DAYS = 2 # кол-во дней для хранения кода активации

# для отправки кода активации
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'info@google.ru'
