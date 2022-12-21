from django.db import models
from django.contrib.auth.models import User
from accounts.utils import sendTransaction
import hashlib

# Create your models here.

# Classe che attribuisce l'IP e la data di accesso
class IpAddress(models.Model):
    pub_date = models.DateTimeField('date published')
    ip_address = models.GenericIPAddressField()

# Classe per creare oggetti con relativi dati di consumo e energia prodotta, 
# con il metodo writeOnChain si scrive nella chain i suddetti dati
class Consumi(models.Model):
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