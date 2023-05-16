from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['10.0.1.180']


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST': get_secret('HOST'),
        'PORT': '5432',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR.parent / 'static' ]
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_URL = "/media/"

# Email Settings
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending
EMAIL_HOST = 'mail.cuasa.hn'
# Port for sending
EMAIL_PORT = 587
# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = get_secret('EMAIL_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_PSW')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/webapps/entorno_cuasa/logs/log-django.txt',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'cuasa_soft': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}