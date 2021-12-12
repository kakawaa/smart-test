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

class AutomationTaskContent(models.Model):
    """API自动化任务内容表"""
    id = models.AutoField(primary_key=True)
    taskname = models.CharField(max_length=32)
    apiname = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    status = models.TextField(default='待执行')
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.apiname)

class AutomationTaskCase(models.Model):
    """API自动化任务用例表"""
    id = models.AutoField(primary_key=True)
    taskname = models.CharField(max_length=32)
    apiname = models.CharField(max_length=32)
    casename = models.TextField(default='用例1')
    status = models.TextField(default='待执行')
    case_type = models.TextField(default='Get')
    request_content = models.TextField(null=True)
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.apiname)

class AutomationTaskCaseAssert(models.Model):
    """API自动化任务用例校验参数表"""
    id = models.AutoField(primary_key=True)
    taskname = models.CharField(max_length=32)
    apiname = models.CharField(max_length=32)
    casename = models.TextField(default='用例1')
    parameter = models.TextField(default='code')
    value = models.TextField(default='200')
    assert_type = models.TextField(default='==')
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.casenum)

class AutomationTaskReport(models.Model):
    """API自动化任务报告表"""
    id = models.AutoField(primary_key=True)
    taskname = models.CharField(max_length=32)
    apiname = models.CharField(max_length=32)
    success_num = models.IntegerField(default=0)
    error_num = models.IntegerField(default=0)
    runner = models.TextField(default='自动化')
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.apiname)