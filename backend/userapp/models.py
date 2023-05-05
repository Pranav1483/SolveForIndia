from django.db import models
from hashlib import sha256
from django.contrib.postgres.fields import HStoreField


class Block(models.Model):
    owner = models.CharField(default='N/A')
    num = models.IntegerField()
    pd_id = models.CharField(max_length=10)
    batch_id = models.CharField(max_length=10)
    timestamp = models.CharField(max_length=30)
    product_details = HStoreField()
    hash_code = models.CharField(max_length=100, unique=True)

class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, blank=True)

class Reports(models.Model):
    username = models.CharField(max_length=32)
    loc = models.CharField(max_length=32)
    report = models.CharField(max_length=500)
    timestamp = models.CharField(max_length=50)


    
