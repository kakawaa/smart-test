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

class INFO(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def apk_info_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/apk/apk_info.html',locals())

    @classmethod
    def get_apk_info_api(cls,request):
        """获取apk信息api"""
        project = common.request_method(request, "project")

        result = {'status': 1, 'apk_info': common.get_apk_info()}
        # result = {'status': 0, 'msg': 1}
        return HttpResponse(json.dumps(result), content_type="application/json")


class VIRUS_SCAN(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def virus_scan_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/apk/virus_scan.html',locals())

class REINFORCE(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def reinforce_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/apk/reinforce.html',locals())
