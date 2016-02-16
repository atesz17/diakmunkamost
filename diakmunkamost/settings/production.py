from .base import *

# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

SECRET_KEY = get_env_variable('DIAKMUNKAMOST_SECRET_KEY')

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [get_env_variable('DIAKMUNKAMOST_ALLOWED_HOSTS')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DIAKMUNKAMOST_DB_NAME'),
        'USER': get_env_variable('DIAKMUNKAMOST_DB_USER'),
        'PASSWORD': get_env_variable('DIAKMUNKAMOST_DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}
