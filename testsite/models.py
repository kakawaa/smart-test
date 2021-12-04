# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    """用户信息表"""
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    nickname = models.CharField(max_length=32,default='')
    avatar = models.TextField(null=True)
    super_admin = models.BooleanField(default=False)
    admin_type = models.CharField(max_length=32,default='')
    mobile = models.TextField(null=True)
    token = models.TextField(null=True)
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.username)

class Log(models.Model):
    """用户日志表"""
    id = models.AutoField(primary_key=True)
    avatar = models.TextField(null=True)
    username = models.CharField(max_length=32)
    page = models.CharField(max_length=32)
    action = models.CharField(max_length=32)
    content = models.TextField(null=True)
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.username)

class AutomationTask(models.Model):
    """API自动化任务表"""
    id = models.AutoField(primary_key=True)
    taskname = models.CharField(max_length=32)
    success_num = models.IntegerField(default=0)
    error_num = models.IntegerField(default=0)
    sum_num = models.IntegerField(default=0)
    status = models.TextField(default='offline')
    timer_type = models.TextField(null=True)
    timer_value = models.TextField(null=True)
    owner = models.TextField(null=True)
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.taskname)
