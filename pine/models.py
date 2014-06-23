from django.db import models
from django.core import validators


class Users(models.Model):
    phone = models.CharField(max_length=15)
    friends = models.ManyToManyField('self', symmetrical=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def __str__(self):
        friends = ''
        for friend in self.friends.all():
            if friends != '':
                friends += ', ' + str(friend.id)
            else:
                friends = str(friend.id)
        return ('pk: ' + str(self.pk)
                + ', phone: ' + self.phone
                + ', friends: [' + friends
                + '], followings: [' + self.followings
                + ']')


class Threads(models.Model):
    author = models.ForeignKey(Users, related_name='authorized')
    is_public = models.BooleanField()
    readers = models.ManyToManyField(Users, related_name='readable')
    pub_date = models.DateTimeField()
    image_url = models.CharField(max_length=256)
    content = models.CharField(max_length=200)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        readers = ''
        for reader in self.readers.all():
            if readers != '':
                readers += ', ' + str(reader.id)
            else:
                readers = str(reader.id)

        return ('pk: ' + str(self.pk)
                + ', author: ' + str(self.author.id)
                + ', is_public:' + str(self.is_public)
                + ', readers: [' + readers
                + '], pub_date: ' + str(self.pub_date)
                + ', image_url: ' + self.image_url
                + ', content: ' + self.content)
