"""
Django settings for sendboro project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, socket, platform
from django.conf.global_settings import STATIC_ROOT, SESSION_ENGINE
from django.template.defaultfilters import addslashes

#setting DB_HOST according to plaform
if platform.system() == 'Linux':
    DB_HOST = 'borobase'
    CACHE_LOC = 'borocache:11211'
    DEBUG = False
else:
    DB_HOST = 'localhost'
    CACHE_LOC = '127.0.0.1:11211'
    DEBUG = True

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__) , '../..'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#&!l7951^bj-p^30z0_lwl&up5hem+u%a_lrhkz6ev3a&c3$nm'

# SECURITY WARNING: don't run with debug turned on in production!


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'template'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = (os.path.join(BASE_DIR, '../static'),)

ALLOWED_HOSTS = []

GEOIP_PATH = os.path.abspath(os.path.join(BASE_DIR, './extras/db'))

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authmod',
    'common',
    'control',
    'home',
    'file',
    'com',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sendboro.urls'

WSGI_APPLICATION = 'sendboro.wsgi.application'


# cache settings for memcached

CACHES = {
         'default' : {
            'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': CACHE_LOC,
         },
         
}

# using a cached DB for session handling

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

#static root is empty so that gunicorn doesn't serves static files
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

APPEND_SLASH = False

MEDIA_ROOT = os.path.join(BASE_DIR, '../media')

MEDIA_URL = '/content/'

DJANGORESIZED_DEFAULT_QUALITY = 99

import dj_database_url

#DATABASES={}
#DATABASES['default'] =  dj_database_url.config()
DATABASES = {
        'default' : {
                  'ENGINE': 'django.db.backends.postgresql_psycopg2',
                  'HOST': DB_HOST,
                  'NAME': 'sendboro',                      
                  'USER': 'postgres',
                  'PASSWORD': 'gungun',
            }
    }

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

SHORT_URL_LENGTH = 4
SHORT_URL_BASEHOST = 'http://sndbr.me'
    