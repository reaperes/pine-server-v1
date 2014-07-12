from PineServerProject.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pine',
        'USER': 'pine',
        'PASSWORD': 'shltlsrudwjfeks',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}