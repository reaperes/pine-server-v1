from django.db import models
import datetime
from django.utils import timezone


# Create your models here.
class Thread(models.Model):
    author = models.CharField(max_length=15)    # need to remodeling, should use foreign key
    content = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    def __str__(self):
        return 'pk: '+str(self.pk)+', pub_date: '+str(self.pub_date)+', content: '+self.content


class Comment(models.Model):
    thread = models.ForeignKey(Thread)
    content = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.content
