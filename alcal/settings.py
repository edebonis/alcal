"""
Django settings for alcal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j2kogo(g2dz59f3*g2^_xjbx3105i2#zqdecgo3yo^%owl280x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []



# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'grappelli',
    'grappelli.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'smart_selects',
    'alumnos',
    'docentes',
    'escuela',
    'asistencias',
    'calificaciones',
    'observaciones',
    'django_extensions',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    )

ROOT_URLCONF = 'alcal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True,
        },
    },
]

WSGI_APPLICATION = 'alcal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#DATABASES = {
#    'default': dj_database_url.config(
#                        default='postgres://sag:sag@localhost:5432/sag')
#}

DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sag',  
        'USER': 'sag',  
        'PASSWORD': 'sag',  
        'HOST': '127.0.0.1',  
        'PORT': '5432',  
    }  
}  



ALLOWED_HOSTS = ['*']
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)
LANGUAGE_CODE = 'ES'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'alcal/static')  
STATIC_URL = '/static/'  
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
GRAPPELLI_ADMIN_TITLE = 'Alcal'

# Settings propios de esta instalacion:
try:
    from .settings_local import *
except ImportError:
    pass
GRAPPELLI_INDEX_DASHBOARD = 'alcal.dashboard.CustomIndexDashboard'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'