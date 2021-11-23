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

class API(View):


    @classmethod
    @method_decorator(Decorators.check_login)
    def post_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/api.html',locals())


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
        print(url)

        payload = json.loads(payload)
        print(payload)
        get_response = common.post(url,**payload)
        code = get_response[0]
        response_txt = get_response[1]
        result = {'status': 1, 'code': code, 'response_txt': response_txt}
        return HttpResponse(json.dumps(result), content_type="application/json")