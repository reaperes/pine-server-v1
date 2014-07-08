from django.db import models


class Users(models.Model):
    phone = models.CharField(max_length=15)
    friends = models.ManyToManyField('self', symmetrical=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    blocks = models.ManyToManyField('self', symmetrical=False, related_name='blocked')

    def __str__(self):
        return ('pk: ' + str(self.pk)
                + ', phone: ' + self.phone
                + ', friends: [' + ' '.join(str(n) for n in [user.id for user in self.friends.only('id')])
                + '], followings: [' + ' '.join(str(n) for n in [user.id for user in self.followings.only('id')])
                + '], blocks: [' + ' '.join(str(n) for n in [user.id for user in self.blocks.only('id')])
                + ']')
