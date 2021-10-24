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

class Home(View):

    @classmethod
    def home_page(cls,request):
        return render(request, 'elver/home.html')

