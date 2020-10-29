"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import datetime
import os

from dotenv import load_dotenv

# Https turn ON/OFF
os.environ['HTTPS'] = "off"
os.environ['wsgi.url_scheme'] = "http"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "http")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Read .env file, parse the contents
load_dotenv(verbose=DEBUG)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


SECURE_SSL_REDIRECT = False

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'notifications',
    'drf_yasg',
    'fcm_django',

    # Local
    'apps.commons.apps.CommonsConfig',
    'apps.wallet.apps.WalletConfig',
    'apps.users.apps.UsersConfig',
    'apps.banks.apps.BanksConfig',
    'apps.exchange',
    'apps.accounts',
    'apps.statistics.apps.StatisticsConfig',
    'apps.reports.apps.ReportsConfig',
    'apps.pricesource.apps.PricesourceConfig',
    'apps.notification.apps.NotificationConfig',
]

CORS_ORIGIN_ALLOW_ALL = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "live.curs-valutar.xyz",
    "www.live.curs-valutar.xyz"
]

CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8015",
    "http://localhost:8001",
    "http://localhost:8015"
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token',
    'cache-control'
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'curs_valutar',
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT'),
#     }
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7)
}

JWT_AUTH = {
    # how long the original token is valid for
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=2),

    # allow refreshing of tokens
    'JWT_ALLOW_REFRESH': True,

    # this is the maximum time AFTER the token was issued that
    # it can be refreshed.  exprired tokens can't be refreshed.
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Bank parser stuff
BANK_PARSER_HOST = os.getenv('BANK_PARSER_HOST')
BANK_PARSER_PORT = os.getenv('BANK_PARSER_PORT')
BANK_PARSER_USERNAME = os.getenv('BANK_PARSER_USERNAME')
BANK_PARSER_PASSWORD = os.getenv('BANK_PARSER_PASSWORD')
BANK_PARSER_DATE_FORMAT = '%Y-%m-%d'
BANK_PARSER_SCHEMA = {
    "type": "object",
    "properties": {
        "bank": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "short_name": {"type": "string"},
            },
        },
        "currency": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "abbr": {"type": "string"},
            },
        },
        "rate_sell": {"type": "number"},
        "rate_buy": {"type": "number"},
        "date": {"type": "string"},
    },
}

HOST_URL = os.getenv('HOST_URL')

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# NGINX - alias /var/path/to/basedir/static/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

ELASTIC = {
    'hosts': 'es-internship.devebs.net',
}

WKHTMLTOPDF_CMD_OPTIONS = {
    'quiet': False,
}

WKHTMLTOPDF_CMD = '/usr/local/bin/wkhtmltopdf'

ELASTICSEARCHENABLED = False

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": os.getenv('FCM_SERVER_KEY')
}
