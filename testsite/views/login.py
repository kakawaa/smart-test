# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import auth
import json
from testsite import models
from testsite.public.common import common
from django.http import HttpResponse
import requests
import sys
sys.getdefaultencoding()

common = common()

class Login(View):

    @classmethod
    def login_page(cls,request):
        return render(request, 'elver/sign-in.html')


    @classmethod
    def login_api(cls,request):
        """账号密码登录"""
        username = common.request_method(request,'username')
        password = common.request_method(request,'password')
        user = models.User.objects.filter(username=username, password=password)
        if user:
            # 登录成功
            # 1，生成特殊字符串
            # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
            # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
            request.session['is_login'] = '1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
            request.session['username'] = username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
            nickname = models.User.objects.filter(username=username, password=password).values("nickname").first()[
                'nickname']
            request.session['nickname'] = nickname
            result = {'code': 200, 'msg': 'old password wrong!'}
        else:
            result = {'code': 202, 'msg': 'old password wrong!'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def sign_up_page(cls, request):
        """账号注册页面"""
        return render(request, 'elver/sign-up.html')

    @classmethod
    def sign_up_api(cls, request):
        """账号注册api"""
        username = common.request_method(request, 'username')
        password = common.request_method(request, 'password')
        user = models.User.objects.filter(username=username, password=password)
        if user:
            result = {'code': 202, 'msg': '账号已经存在'}
        else:
            models.User(username=username, password=password,nickname=username).save()
            result = {'code': 200, 'msg': '创建账号成功'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def logout(cls,request):
        """退出登录"""
        auth.logout(request)
        response = redirect('/login/')
        return response