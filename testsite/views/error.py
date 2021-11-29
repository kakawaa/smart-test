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

class CommonError(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def error_404_page(cls,request,exception):
        return render(request, 'elver/error/404.html')

    @classmethod
    @method_decorator(Decorators.check_login)
    def error_500_page(cls, request):
        return render(request, 'elver/error/500.html')
