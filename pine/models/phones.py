from django.db import models


class Phones(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)

    class Meta:
        app_label = 'pine'

    def __str__(self):
        return ('pk: ' + str(self.pk)
                + ', phone_number: ' + self.phone_number)
