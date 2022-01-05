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
    timer_switch = models.TextField(default='',null=True)
    ding_token = models.TextField(default='',null=True)
    ding_switch = models.TextField(default='',null=True)
    owner = models.TextField(null=True)
    task_user = models.TextField(default='')
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.taskname)

class AutomationTaskUser(models.Model):
    """API自动化任务用户表"""
    id = models.AutoField(primary_key=True)
    taskname = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    avatar = models.TextField(null=True)
    role = models.CharField(max_length=64)
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.taskname)

class AutomationTaskContent(models.Model):
    """API自动化任务内容表"""
    id = models.AutoField(primary_key=True)
    run_id = models.TextField(default='NA')
    taskname = models.CharField(max_length=32)
    apiname = models.CharField(max_length=32)
    url = models.TextField(default='')
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
    assert_type_id = models.TextField(default='')
    assert_id = models.TextField(default='')
    parameter_id = models.TextField(default='')
    value_id = models.TextField(default='')
    debug_id = models.TextField(default='')
    del_id = models.TextField(default='')
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.casenum)


class AutomationTaskResult(models.Model):
    """API自动化任务结果表"""
    id = models.AutoField(primary_key=True)
    run_id = models.TextField(default='')
    taskname = models.TextField()
    apiname = models.TextField()
    casename = models.TextField()
    status = models.TextField()
    parameter = models.TextField()
    assert_type = models.TextField()
    pre_value = models.TextField()
    final_value = models.TextField(null=True)
    response = models.TextField(null=True)
    runner = models.TextField(default='自动化')
    error = models.TextField(default='')
    ctime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return ' %s' % ( self.apiname)