from django.db import models

from pine.models.phones import Phones


class Auths(models.Model):
    phone = models.OneToOneField(Phones)
    auth_number = models.CharField(max_length=6)

    class Meta:
        app_label = 'pine'

    def __str__(self):
        return ('pk: ' + str(self.pk)
                + ', phone: ' + str(self.phone)
                + ', auth_number: ' + self.auth_number)
