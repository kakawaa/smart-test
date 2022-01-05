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

class Document(View):

    @classmethod
    @method_decorator(Decorators.catch_except)
    def document_page(cls,request,*arg,**kwargs):
        path = kwargs['path']
        return render(request, f'elver/doc/{path}.html',locals())

