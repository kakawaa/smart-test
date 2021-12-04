# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
import os
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import auth
import json
from testsite import models
from testsite.public.common import common
from testsite.public.decorators import Decorators
from django.http import HttpResponse
import requests
import sys
import time
sys.getdefaultencoding()

common = common()

class API_POST(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def post_page(cls,request):
        """手工测试主页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/api/api.html',locals())


    @classmethod
    def demo_api(cls, request):
        """demo api"""
        user = common.request_method(request, "user")
        result = {'status': 1, 'name': user,'age':18}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def get_response_api(cls, request):
        """获取接口返回api"""
        url = common.request_method(request, "url")
        payload = common.request_method(request, "payload")
        payload = json.loads(payload)
        get_response = common.post(url,**payload)
        code = get_response[0]
        response_txt = get_response[1]
        result = {'status': 1, 'code': code, 'response_txt': response_txt}
        return HttpResponse(json.dumps(result), content_type="application/json")

class API_TASK(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def task_page(cls,request):
        """自动化测试主页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        tasks = models.AutomationTask.objects.all().order_by('-id')
        return render(request, 'elver/api/api_task.html',locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    def task_more_page(cls, request,*arg,**kwargs):
        """自动化任务配置页"""
        taskname = kwargs['taskname']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/api/api_task_more.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    def task_content_page(cls,request,*arg,**kwargs):
        """自动化任务内容页"""
        taskname = kwargs['taskname']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/api/api_task_content.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    def api_case_page(cls, request, *arg, **kwargs):
        """自动化用例页"""
        taskname = kwargs['taskname']
        apiname = kwargs['apiname']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/api/api_case.html', locals())

    @classmethod
    def create_task_api(cls, request):
        """创建任务接口"""
        taskname = common.request_method(request, "taskname")
        username = request.session['username']
        task_num = models.AutomationTask.objects.filter(taskname=taskname).count()
        if task_num == 0:
            models.AutomationTask(taskname=taskname,owner=username).save()
            result = {'status': 1, 'msg': '创建任务成功'}
        else:
            result = {'status': 0, 'msg': '该任务已存在'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def get_task_api(cls, request):
        """获取任务信息接口"""
        taskname = common.request_method(request, "taskname")
        if taskname:
            success_num = models.AutomationTask.objects.filter(taskname=taskname).values("success_num").first()[
                'success_num']
            error_num = models.AutomationTask.objects.filter(taskname=taskname).values("error_num").first()['error_num']
            sum_num = models.AutomationTask.objects.filter(taskname=taskname).values("sum_num").first()['sum_num']
            status = models.AutomationTask.objects.filter(taskname=taskname).values("status").first()['status']
            timer_type = models.AutomationTask.objects.filter(taskname=taskname).values("timer_type").first()[
                'timer_type']
            timer_value = models.AutomationTask.objects.filter(taskname=taskname).values("timer_value").first()[
                'timer_value']
            owner = models.AutomationTask.objects.filter(taskname=taskname).values("owner").first()['owner']
            task_data = {
                "success_num": success_num,
                "error_num": error_num,
                "sum_num": sum_num,
                "status": status,
                "timer_type": timer_type,
                "timer_value": timer_value,
                "owner":owner
            }
            result = {'status': 1, 'data': task_data}
        else:
            result = {'status': 0, 'msg': 'taskname is empty'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def delete_task_api(cls, request):
        """删除任务接口"""
        taskname = common.request_method(request, "taskname")
        username = request.session['username']
        owner = models.AutomationTask.objects.filter(taskname=taskname).values("owner").last()['owner']
        if owner == username:
            models.AutomationTask.objects.filter(taskname=taskname).delete()
            result = {'status': 1, 'msg': '删除成功！'}
        else:
            result = {'status': 0, 'msg': '不是OWNER,无法操作!'}
        return HttpResponse(json.dumps(result), content_type="application/json")

class API_STRESS_TEST(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def stress_test_page(cls,request):
        """压力测试主页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/api/api_stress_test.html',locals())