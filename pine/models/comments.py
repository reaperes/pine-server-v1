from django.db import models

from pine.models.users import Users
from pine.models.threads import Threads


class Comments(models.Model):
    author = models.ForeignKey(Users)
    thread = models.ForeignKey(Threads)
    likes = models.ManyToManyField(Users, related_name='likeComments')
    reports = models.ManyToManyField(Users, related_name='reportComments')
    pub_date = models.DateTimeField()
    content = models.CharField(max_length=200)

    class Meta:
        app_label = 'pine'
        ordering = ['-pub_date']

    def __str__(self):
        return ('pk: ' + str(self.pk)
                + ', author: ' + str(self.author.id)
                + ', likes: [' + ' '.join(str(n) for n in [user.id for user in self.likes.only('id')])
                + '], reports: [' + ' '.join(str(n) for n in [user.id for user in self.reports.only('id')])
                + '], pub_date: ' + str(self.pub_date)
                + ', content: ' + self.content)
