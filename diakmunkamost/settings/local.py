from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6tw2gz^r_v#rl&zq*!3&5l^d7g7h^&nq13r=icnya0t7*73*r^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'diakmunkamost_local',
        'USER': 'localuser',
        'PASSWORD': 'local123',
        'HOST': 'localhost',
        'PORT': '',
    }
}
