from django.db import models

# Create your models here.

class IpAddress(models.Model):
    pub_date = models.DateTimeField('date published')
    ip_address = models.GenericIPAddressField()