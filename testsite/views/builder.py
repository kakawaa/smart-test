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

class Builder(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def builder_page(cls,request,*arg,**kwargs):
        home_path = kwargs['home_path']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/builder/builder.html',locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def builder_detail_page(cls, request,*arg,**kwargs):
        jobname = kwargs['jobname']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/builder/builder-detail.html',locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def builder_step_page(cls, request,*arg,**kwargs):
        jobname = kwargs['jobname']
        item = kwargs['item']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/builder/builder-steps.html',locals())

