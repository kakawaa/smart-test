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

class APM_TEST(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def test_page(cls,request):
        """APM测试页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/apm/apm_test.html',locals())


class APM_REPORT(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def report_home_page(cls,request):
        """云端报告主页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/apm/apm_report.html',locals())