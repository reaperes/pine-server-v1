from django.db import models

from pine.models.phones import Phones


class Users(models.Model):
    phone = models.OneToOneField(Phones)
    friend_phones = models.ManyToManyField(Phones, related_name='related_phone_user')
    friends = models.ManyToManyField('self', symmetrical=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    blocks = models.ManyToManyField('self', symmetrical=False, related_name='blocked')

    class Meta:
        app_label = 'pine'

    def __str__(self):
        return ('pk: ' + str(self.pk)
                + ', phone: ' + self.phone.phone_number
                + ', friend_phones: ' + ' '.join(str(n) for n in [phone.id for phone in self.friend_phones.only('id')])
                + ', friends: [' + ' '.join(str(n) for n in [user.id for user in self.friends.only('id')])
                + '], followings: [' + ' '.join(str(n) for n in [user.id for user in self.followings.only('id')])
                + '], blocks: [' + ' '.join(str(n) for n in [user.id for user in self.blocks.only('id')])
                + ']')
