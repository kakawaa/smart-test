# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    """User"""
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    nickname = models.CharField(max_length=32,default='')
    super_admin = models.BooleanField(default=False)
    admin_type = models.CharField(max_length=32,default='')
    anm = models.TextField(null=True)
    aab_anm = models.TextField(null=True)
    head_image =  models.TextField(null=True)
    mobile = models.TextField(null=True)
    token = models.TextField(null=True)
    current_anm = models.TextField(default='TI')
    theme_mode =  models.TextField(null=True)
    error_info =  models.TextField(null=True)
    ctime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ' %s' % ( self.username)
