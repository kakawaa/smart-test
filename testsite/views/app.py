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

class FeedBack(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def feedback_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/app/feedback.html',locals())

class Action(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def action_log_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/app/action_log.html',locals())

class APP_LOG(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def app_log_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/app/app_log.html',locals())

class Crash(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def crash_log_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/app/crash_log.html',locals())