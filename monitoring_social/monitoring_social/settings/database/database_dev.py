from monitoring_social.config.config_dev import (
    NAME,
    USER,
    PASSWORD,
    HOST,
    PORT
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
    }
}