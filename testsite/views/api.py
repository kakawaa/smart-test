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
        return render(request, 'elver/api/api_task.html',locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    def task_content_page(cls,request,*arg,**kwargs):
        """自动化测试主页"""
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
        """自动化测试主页"""
        taskname = kwargs['taskname']
        apiname = kwargs['apiname']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/api/api_case.html', locals())

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