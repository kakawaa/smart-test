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
import time
sys.getdefaultencoding()

common = common()

class API_POST(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def post_page(cls,request):
        """手工测试主页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/api/api.html',locals())


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
        payload = json.loads(payload)
        get_response = common.post(url,**payload)
        code = get_response[0]
        response_txt = get_response[1]
        result = {'status': 1, 'code': code, 'response_txt': response_txt}
        return HttpResponse(json.dumps(result), content_type="application/json")

class API_TASK(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def task_page(cls,request):
        """自动化测试主页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        tasks = models.AutomationTask.objects.all().order_by('-id')
        task_num = models.AutomationTaskContent.objects.all().count()
        return render(request, 'elver/api/api_task.html',locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    def task_more_page(cls, request,*arg,**kwargs):
        """自动化任务配置页"""
        taskname = kwargs['taskname']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/api/api_task_more.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    def task_content_page(cls,request,*arg,**kwargs):
        """自动化任务内容页"""
        taskname = kwargs['taskname']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        apis = models.AutomationTaskContent.objects.filter(taskname=taskname).order_by('-id')
        api_num = models.AutomationTaskContent.objects.filter(taskname=taskname).count()
        return render(request, 'elver/api/api_task_content.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    def api_case_page(cls, request, *arg, **kwargs):
        """自动化用例页"""
        taskname = kwargs['taskname']
        apiname = kwargs['apiname']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        cases = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname).order_by('id')
        case_num = models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname).count()
        if case_num > 0:
            casename = kwargs['casename']
            case_type = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).values("case_type").first()['case_type']
            case_asserts = models.AutomationTaskCaseAssert.objects.filter(taskname=taskname,apiname=apiname,casename=casename).order_by('id')
        return render(request, 'elver/api/api_case.html', locals())

    @classmethod
    def create_task_api(cls, request):
        """创建任务接口"""
        taskname = common.request_method(request, "taskname")
        username = request.session['username']
        task_num = models.AutomationTask.objects.filter(taskname=taskname).count()
        if task_num == 0:
            models.AutomationTask(taskname=taskname,owner=username).save()
            result = {'status': 1, 'msg': '创建任务成功'}
        else:
            result = {'status': 0, 'msg': '该任务已存在'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def get_task_api(cls, request):
        """获取任务信息接口"""
        taskname = common.request_method(request, "taskname")
        if taskname:
            success_num = models.AutomationTask.objects.filter(taskname=taskname).values("success_num").first()[
                'success_num']
            error_num = models.AutomationTask.objects.filter(taskname=taskname).values("error_num").first()['error_num']
            sum_num = models.AutomationTask.objects.filter(taskname=taskname).values("sum_num").first()['sum_num']
            status = models.AutomationTask.objects.filter(taskname=taskname).values("status").first()['status']
            timer_type = models.AutomationTask.objects.filter(taskname=taskname).values("timer_type").first()[
                'timer_type']
            timer_value = models.AutomationTask.objects.filter(taskname=taskname).values("timer_value").first()[
                'timer_value']
            owner = models.AutomationTask.objects.filter(taskname=taskname).values("owner").first()['owner']
            task_data = {
                "success_num": success_num,
                "error_num": error_num,
                "sum_num": sum_num,
                "status": status,
                "timer_type": timer_type,
                "timer_value": timer_value,
                "owner":owner
            }
            result = {'status': 1, 'data': task_data}
        else:
            result = {'status': 0, 'msg': 'taskname is empty'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def get_newcase_api(cls, request):
        """获取api最新用例名称接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        case_num = models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname).count()
        if taskname and apiname:
            if case_num>0:
                newest_case = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname).values("casename").first()['casename']
                result = {'status': 1, 'newest_case': newest_case}
            else:
                result = {'status': 1, 'newest_case': 'no case'}
        else:
            result = {'status': 0, 'msg': 'taskname is empty'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def run_task_api(cls, request):
        """执行任务接口"""
        taskname = common.request_method(request, "taskname")
        new_status = common.request_method(request, "new_status")
        username = request.session['username']
        try:
            models.AutomationTask.objects.filter(taskname=taskname).update(status=new_status)
            result = {'status': 1, 'msg': '开始执行！'}
        except Exception as e:
            result = {'status': 0, 'msg': e}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def delete_task_api(cls, request):
        """删除任务接口"""
        taskname = common.request_method(request, "taskname")
        username = request.session['username']
        owner = models.AutomationTask.objects.filter(taskname=taskname).values("owner").last()['owner']
        api_num = models.AutomationTaskContent.objects.filter(taskname=taskname).count()
        if owner == username and api_num == 0:
            models.AutomationTask.objects.filter(taskname=taskname).delete()
            result = {'status': 1, 'msg': '删除成功！'}
        else:
            if owner != username:
                result = {'status': 0, 'msg': '不是OWNER,无法操作!'}
            else:
                result = {'status': 0, 'msg': '该任务下有接口数>0'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def create_task_content_api(cls, request):
        """创建任务内容接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        url = common.request_method(request, "url")
        username = request.session['username']
        api_num = models.AutomationTaskContent.objects.filter(taskname=taskname,apiname=apiname).count()
        if api_num == 0:
            models.AutomationTaskContent(taskname=taskname, apiname=apiname,url=url).save()
            result = {'status': 1, 'msg': '创建接口成功'}
        else:
            result = {'status': 0, 'msg': '该接口已存在'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def edit_task_content_api(cls, request):
        """编辑任务api接口"""
        id = common.request_method(request, "id")
        new_apiname = common.request_method(request, "new_apiname")
        new_url = common.request_method(request, "new_url")
        username = request.session['username']
        ctime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        try:
            models.AutomationTaskContent.objects.filter(id=id).update(apiname=new_apiname, url=new_url,ctime=ctime)
            result = {'status': 1, 'msg': '更新成功！'}
        except Exception as e:
            result = {'status': 0, 'msg':e}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def set_task_content_status_api(cls, request):
        """更新任务api状态接口"""
        id = common.request_method(request, "id")
        new_status = common.request_method(request, "new_status")
        username = request.session['username']
        ctime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        try:
            models.AutomationTaskContent.objects.filter(id=id).update(status=new_status,ctime=ctime)
            result = {'status': 1, 'msg': '更新成功！'}
        except Exception as e:
            result = {'status': 0, 'msg': e}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def delete_task_content_api(cls, request):
        """删除任务api接口"""
        id = common.request_method(request, "id")
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        username = request.session['username']
        models.AutomationTaskContent.objects.filter(id=id).delete()
        models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname).delete()
        models.AutomationTaskCaseAssert.objects.filter(taskname=taskname,apiname=apiname).delete()
        result = {'status': 1, 'msg': '删除成功！'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def create_task_case_api(cls, request):
        """创建任务用例接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        case_type = common.request_method(request, "case_type")
        casename = common.request_method(request, "casename")
        username = request.session['username']
        case_num = models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname,casename=casename).count()
        if case_num == 0:
            models.AutomationTaskCase(taskname=taskname, apiname=apiname, case_type=case_type,casename=casename).save()
            result = {'status': 1, 'msg': '创建用例成功'}
        else:
            result = {'status': 0, 'msg': '该用例名称已存在'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    def delete_task_case_api(cls, request):
        """删除任务用例接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        casename = common.request_method(request, "casename")
        username = request.session['username']
        models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).delete()
        models.AutomationTaskCaseAssert.objects.filter(taskname=taskname,apiname=apiname,casename=casename).delete()
        case_num = models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname).count()
        if case_num > 0:
            first_casename = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname).values("casename").first()['casename']
            result = {'status': 1, 'msg': '删除成功！','first_casename':first_casename}
        else:
            result = {'status': 1, 'msg': '删除成功！', 'first_casename': 'no case'}
        return HttpResponse(json.dumps(result), content_type="application/json")

class API_STRESS_TEST(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    def stress_test_page(cls,request):
        """压力测试主页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
        return render(request, 'elver/api/api_stress_test.html',locals())