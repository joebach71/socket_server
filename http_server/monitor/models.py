from django.db import models

# Create your models here.
class Storage(models.Model):
    '''
    Data stored by memcached is identified with the help of a key. A key
    is a text string which should uniquely identify the data for clients
    that are interested in storing and retrieving it.  Currently the
    length limit of a key is set at 250 characters (of course, normally
    clients wouldn't need to use such long keys); the key must not include
    control characters or whitespace.
    '''
    key = models.CharField(max_length=250, unique=True)
    value = models.TextField()
    flags = models.CharField(max_length=10)
    exptime = models.IntegerField()
    size = models.IntegerField()
