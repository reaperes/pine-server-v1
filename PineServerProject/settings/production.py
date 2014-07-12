from PineServerProject.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pine',
        'USER': 'pine',
        'PASSWORD': 'shltlsrudwjfeks',
        'HOST': '125.209.194.90',
        'PORT': '3306',
    }
}