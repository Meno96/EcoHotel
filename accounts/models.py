from django.db import models
from django.contrib.auth.models import User
from accounts.utils import sendTransaction
import hashlib

# Create your models here.

class IpAddress(models.Model):
    pub_date = models.DateTimeField('date published')
    ip_address = models.GenericIPAddressField()

class Consumi(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    produced_energy_in_watt = models.TextField()
    consumed_energy_in_watt = models.TextField()
    hash = models.CharField(max_length=32, default=None, null=True)
    hash2 = models.CharField(max_length=32, default=None, null=True)
    txId=models.CharField(max_length=66, default=None, null=True)

    def writeOnChain(self):
        self.hash=hashlib.sha256(self.produced_energy_in_watt.encode('utf-8')).hexdigest()
        self.hash2=hashlib.sha256(self.consumed_energy_in_watt.encode('utf-8')).hexdigest()
        self.txId=sendTransaction(self.produced_energy_in_watt + '\n' + self.consumed_energy_in_watt)
        self.save()