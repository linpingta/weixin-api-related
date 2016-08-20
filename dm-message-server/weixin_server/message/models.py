from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TaskContentModel(models.Model):
    name = models.CharField(max_length=100)
    AD_CHOICES = (('1', 'campaign'), ('2', 'account'), ('3', 'user-defined'))
    ad_type = models.CharField(max_length=10, choices=AD_CHOICES, default='1')
    condition = models.CharField(max_length=100)
    roi = models.IntegerField()
    CHECK_CHOICES = (('1', 'daily'), ('2', 'lifetime'))
    check_type = models.CharField(max_length=10, choices=CHECK_CHOICES, default='1')
