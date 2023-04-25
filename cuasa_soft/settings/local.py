from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


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
STATIC_ROOT = '/static/'


MEDIA_ROOT = BASE_DIR.parent / 'media'

MEDIA_URL = '/media/'

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
