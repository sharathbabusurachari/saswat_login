import os
import logging
logger = logging.getLogger(__name__)
logger.info('Logging initialized in settings.py')
"""
Django settings for saswat_cust_info project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p$5m!@8&k@4rtj3f+(sxk5xy9!6zpqf$uz)k_c=m1fi%pql-wb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['ci1.saswatfinance.com','*']

# Application definition
DATABASE_ROUTERS = ['routers.SaswatCustAppRouter', 'routers.DataEntryAppRouter']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'saswat_cust_app',
    'saswat_cust_info',
    'rest_framework.authtoken',
    'data_entry_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'saswat_cust_info.urls'

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

WSGI_APPLICATION = 'saswat_cust_info.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
     'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'kaka_postgres',
		'USER': 'postgres_kaka',
	    'PASSWORD': 'postgres_pwd',
	    'HOST': 'localhost',
	    'PORT': 5432,
      },
    'sqlit': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dataentry_db',
        'USER': 'dataentry_user',
        'PASSWORD': 'dataentry_pwd',
        'HOST': 'localhost',
        'PORT': 5432
    },
 }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = '/var/lib/jenkins/workspace/04_Saswat_login_CICD/static'
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles'),]

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/lib/jenkins/workspace/04_Saswat_login_CICD/media'


DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520  # Set maximum request size to 10 megabytes (10 * 1024 * 1024 bytes)
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520  # Set maximum file upload size to 10 megabytes




# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

LOG_DIR = '/var/lib/jenkins/workspace/04_Saswat_login_CICD/logs'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/lib/jenkins/workspace/04_Saswat_login_CICD/logs/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


