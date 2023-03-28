"""
Django settings for TrackYourAlumni project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""


from pathlib import Path
from dotenv import load_dotenv
import os
# import djcelery

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/'.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-r!*(l2jjn%0*ns!b)faqy-4cfrs_)yh2g-4$%9(zwn1+x*6!#z"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
AUTH_USER_MODEL = 'users_auth.CustomUser'

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "phonenumber_field",
    "departments",
    "users_auth",
    "roles_permissions",
    "request_inbox",
    "UrlStored",
    "corsheaders",
    "registration",
    "dashboard",
    "UrlSearch.apps.UrlsearchConfig",
    'crispy_forms',
    'django_celery_results',
    'django_celery_beat',
    'celery_progress',
    "chartjs",
    # "djcelery",
]

CORS_ORIGIN_ALLOW_ALL = True
PHONENUMBER_DEFAULT_REGION='IN'
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
CRISPY_TEMPLATE_PACK = 'uni_form'
ROOT_URLCONF = "TrackYourAlumni.urls"

STATIC_ROOT=os.path.join(BASE_DIR,'static/')
MEDIA_ROOT=os.path.join(BASE_DIR,'media/')

STATICFILES_DIRS=[os.path.join(BASE_DIR,"TrackYourAlumni","static")]

STATIC_URL = "/static/"
MEDIA_URL='/media/'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR,'UrlSerch/templates/'),
            os.path.join(BASE_DIR,'registration/templates/'),
            os.path.join(BASE_DIR,'TrackYourAlumni/templates/'),
            os.path.join(BASE_DIR,'users_auth/templates/'),
            os.path.join(BASE_DIR,'users_auth/templates/registration'),
            os.path.join(BASE_DIR,'dashboard/templates/'),

        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "TrackYourAlumni.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DJANGO_DATABASE_ENGIN"),
        'NAME': os.getenv("DJNAGO_DATABASE_NAME"), 
        'USER': os.getenv("DJANGO_DATABASE_USERNAME"), 
        'PASSWORD': os.getenv("DJANGO_DATABASE_PASSWORD"),
        'HOST': os.getenv("DJANGO_DATABASE_HOST"), 
        'PORT': os.getenv("DJANGO_DATABASE_PORT")
    },

    'DB':{
        'ENGINE': os.getenv("STORED_DATABASE_ENGIN"),
        'NAME':os.getenv("STORED_DATABASE_NAME") , 
        'USER': os.getenv("STORED_DATABASE_USERNAME"), 
        'PASSWORD': os.getenv("STORED_DATABASE_PASSWORD"),
        'HOST': os.getenv("STORED_DATABASE_HOST"), 
        'PORT': os.getenv("STORED_DATABASE_PORT"),
    },
}

#databse name of which store the entry of the new DATABASE of user
DATABASE_STORE_ENTRY='DB'
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "users_auth:user-list"
LOGOUT_REDIRECT_URL = "login"

# email setting

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
DOMAIN = os.getenv("DOMAIN")
EMAIL_USE_SSL =os.getenv("EMAIL_USE_SSL")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")

# djcelery.setup_loader()

#CELERY SETTINGS

CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT=['application/json','pickle']
CELERY_RESULT_SERIALIZER='json'
CELERY_TASK_SERIALIZER='pickle'
CELERY_TIMEZONE=os.getenv("CELERY_TIMEZONE")
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TRACK_STARTED = True


#CELERY BEAT SETTING
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

#GEo Location Key
GEO_KEY=os.getenv("GEO_LOCATION_KEY")

##default Databse for create new Database of University
DEFAULT_DATABASE_ENGIN=os.getenv("DEFAULT_DATABASE_ENGIN")

#default Databse for create new Database of University
DEFAULT_DATABASE_HOST=os.getenv("DEFAULT_DATABASE_HOST")
DEFAULT_DATABASE_PORT=os.getenv("DEFAULT_DATABASE_PORT")
DEFAULT_DATABASE_USERNAME=os.getenv("DEFAULT_DATABASE_USERNAME")
DEFAULT_DATABASE_PASSWORD=os.getenv("DEFAULT_DATABASE_PASSWORD")

#user Information api
USER_NAME1=os.getenv("USER_NAME1")
PASSWORD1=os.getenv("PASSWORD1")

USER_NAME2=os.getenv("USER_NAME2")
PASSWORD2=os.getenv("PASSWORD2")

USER_NAME3=os.getenv("USER_NAME3")
PASSWORD3=os.getenv("PASSWORD3")