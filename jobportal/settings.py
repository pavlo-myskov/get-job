"""
Django settings for jobportal project.

Generated by 'django-admin startproject' using Django 3.2.19.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants as messages

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

development = os.getenv('DEVELOPMENT', False) == 'True'
if development:
    print('Development mode is ON.')
else:
    print('Development mode is OFF.')

DEBUG = os.getenv('DEBUG', False) == 'True'
if DEBUG:
    print('Debug mode is ON.')
else:
    print('Debug mode is OFF.')

SECRET_KEY = os.getenv('SECRET_KEY')


ALLOWED_HOSTS = ['127.0.0.1', 'localhost',
                 'get-job-dev.herokuapp.com',
                 'get-job.herokuapp.com',
                 'get-job.live',
                 'www.get-job.live']

# Clickjacking protection. Means that you can
# only embed your site in an iframe on your own domain.
X_FRAME_OPTIONS = 'SAMEORIGIN'

if development:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    # redirect from http to https on heroku
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    # set session and csrf cookies to secure
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap5',
    'sass_processor',
    'compressor',
    'users',
    'jobseeker',
    'employer',
    'jobs',
    'resumes',
    'notifications',
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

ROOT_URLCONF = 'jobportal.urls'

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

STATICFILES_FINDERS = [
    # Default finders
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # sass processor and compressor finders
    'sass_processor.finders.CssFinder',
]

WSGI_APPLICATION = 'jobportal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if development:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")

    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL')
        )
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ___Static files (CSS, JavaScript, Images)___
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if not development:
    STATIC_URL = '/static/get-job/'

    CLOUDINARY_STORAGE = {
        'CLOUDINARY_URL': os.getenv('CLOUDINARY_URL'),
    }
    STATICFILES_STORAGE = 'cloudinary_storage.storage.'\
        'StaticHashedCloudinaryStorage'

    # URL path for media files where they will be served from
    MEDIA_URL = '/media/get-job/'
    # cloudinary media settings
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # URL path for your static files where they
    # will be served from during development
    STATIC_URL = '/static/'
    # URL path for media files where they will be served from
    MEDIA_URL = '/media/'

# Dir where media files are stored during development
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Dir where your static files are stored during development
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]
# Dir where static files will be collected using
# python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Dir where sass files are stored
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'static')
# ___---___

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Set custom user model as default
AUTH_USER_MODEL = "users.User"


# ___Allauth___

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    ]

ACCOUNT_FORMS = {
    "signup": "users.forms.CustomSignupForm",
    "login": "users.forms.CustomLoginForm",
}

# allows to specify Custom Redirects for signup, login, logout
ACCOUNT_ADAPTER = "users.adapters.CustomAccountAdapter"

SITE_ID = 1

# Specifies the URL that the user will be redirected
# to after a successful login or logout.
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# No e-mail verification is required to complete the signup process.
ACCOUNT_EMAIL_VERIFICATION = 'none'
# Removes the username field from the signup form.
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# Requires the user to enter a unique e-mail address during signup.
ACCOUNT_EMAIL_REQUIRED = True
# Removes the username field from the signup form.
ACCOUNT_USERNAME_REQUIRED = False
# Allows the user to log in using their e-mail address and password.
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# Prevents multiple signups with the same e-mail address.
ACCOUNT_UNIQUE_EMAIL = True
# Disables the e-mail verification when a user signs up.
ACCOUNT_EMAIL_VERIFICATION = 'none'
# asks the user to Remember Me at login to keep the user logged in
# even after closing the browser.
ACCOUNT_SESSION_REMEMBER = None

# TODO: Add email verification:
# email verification is mandatory to complete the signup process
# prevents brute force attacks
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# User gets blocked from logging back in until a timeout.
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5


# ___Crispy bootstrap5___
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Custom message tags for Bootstrap 4, 5
MESSAGE_TAGS = {
        messages.DEBUG: 'secondary',
        messages.INFO: 'info',
        messages.SUCCESS: 'success',
        messages.WARNING: 'warning',
        messages.ERROR: 'danger',
 }
