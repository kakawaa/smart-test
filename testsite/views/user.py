# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
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

class Setting(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def setting_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/setting.html',locals())

class UserActivity(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def user_activity_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/activity.html',locals())