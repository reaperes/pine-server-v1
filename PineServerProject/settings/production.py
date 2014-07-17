from PineServerProject.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pine',
        'USER': 'pine',
        'PASSWORD': 'shltlsrudwjfeks',
        'HOST': '10.12.0.102',
        'PORT': '3306',
    }
}