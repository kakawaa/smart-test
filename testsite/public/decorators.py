import time
from logzero import logger
from django.shortcuts import render,redirect
from testsite import models
from functools import wraps
import traceback

class Decorators(object):

    @classmethod
    def check_login(cls,function):
        """登录检查装饰器"""
        @wraps(function)
        def wrap(request, *arg, **kwargs):
            if request.session.get('is_login') == '1' or request.user.username:
                return function(request, *arg, **kwargs)
            else:
                return redirect('/login/signin')
        return wrap

    @classmethod
    def fun_log(cls,function):
        """记录日志装饰器"""
        @wraps(function)
        def wrap(*arg, **kwargs):
            logger.info(f'call fun {function.__doc__}')
            return function(*arg, **kwargs)
        return wrap

    @classmethod
    def catch_except(cls,function):
        """异常跳转装饰器"""
        @wraps(function)
        def wrap(request,*arg, **kwargs):
            try:
                func = function(request,*arg, **kwargs)
            except:
                username = request.session['username']
                logger.info(f'[{username}]{function} error info:')
                traceback.print_exc()
                models.User.objects.filter(username=username).update(error_info=traceback.format_exc())
                return redirect('/error/')
            else:
                return func
        return wrap


