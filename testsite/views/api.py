# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
import os
import re
from django.views import View
from django.db.models import Q
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
import traceback
sys.getdefaultencoding()

common = common()

class API_POST(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def post_page(cls,request):
        """手工测试主页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
            common.add_user_log(username=username,avatar=avatar,page='手工测试主页',action='查看',content='')    
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
        try:
            url = common.request_method(request, "url")
            payload = common.request_method(request, "payload")
            get_response = common.case_json_post(url,payload)
            code = get_response[0]
            response_txt = get_response[1]
            result = {'status': 1, 'code': code, 'response_txt': response_txt}
        except Exception as e:
            result = {'status': 0, 'msg':str(e)}    
        return HttpResponse(json.dumps(result), content_type="application/json")

class API_TASK(View):

    script_dir = '/home1/www/tomcat/apache-tomcat-9.0.27/webapps/examples/elver/api/script/'
    # script_dir = '/home2/jenkins/smart-test/api/script/'


    # BASE_DIR = os.path.dirname(os.getcwd())
    # script_dir = os.path.join(BASE_DIR, 'elver/testsite/script/')

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def task_page(cls,request):
        """自动化测试主页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        tasks = models.AutomationTask.objects.filter(task_user__contains=username).order_by('-id')
        task_names = models.AutomationTask.objects.filter(task_user__contains=username).values('taskname').distinct()
        task_num = models.AutomationTask.objects.filter(task_user__contains=username).count()
        running_task_num = models.AutomationTaskContent.objects.filter(status='执行中').count()
        return render(request, 'elver/api/api_task.html',locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def task_more_page(cls, request,*arg,**kwargs):
        """自动化任务配置页"""
        taskname = kwargs['taskname']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        timer_switch = models.AutomationTask.objects.filter(taskname=taskname).values("timer_switch").last()['timer_switch']
        timer_value = models.AutomationTask.objects.filter(taskname=taskname).values("timer_value").last()[
            'timer_value']
        ding_switch = models.AutomationTask.objects.filter(taskname=taskname).values("ding_switch").last()[
            'ding_switch']
        ding_token = models.AutomationTask.objects.filter(taskname=taskname).values("ding_token").last()[
            'ding_token']
        task_users = models.AutomationTaskUser.objects.filter(taskname=taskname).order_by('id')
        users = models.User.objects.all().values('username').distinct()
        return render(request, 'elver/api/api_task_more.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def task_content_page(cls,request,*arg,**kwargs):
        """自动化任务内容页"""
        taskname = kwargs['taskname']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        apis = models.AutomationTaskContent.objects.filter(taskname=taskname).order_by('-id')
        api_num = models.AutomationTaskContent.objects.filter(taskname=taskname).count()
        task_result_num =  models.AutomationTaskResult.objects.filter(taskname=taskname).count()
        running_task_num = models.AutomationTaskContent.objects.filter(taskname=taskname,status='执行中').count()
        if task_result_num > 0:
            last_run_id = models.AutomationTaskResult.objects.filter(taskname=taskname).values("run_id").last()['run_id']
        else:
            last_run_id = 'NA'
        api_names = models.AutomationTaskContent.objects.filter(taskname=taskname).values('apiname').distinct()
        return render(request, 'elver/api/api_task_content.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def task_result_page(cls, request, *arg, **kwargs):
        """自动化结果页"""
        taskname = kwargs['taskname']
        apiname = kwargs['apiname']
        run_id = kwargs['run_id']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        report_num = models.AutomationTaskResult.objects.filter(taskname=taskname,apiname=apiname,run_id=run_id).count()
        results = models.AutomationTaskResult.objects.filter(taskname=taskname,apiname=apiname,run_id=run_id).order_by('id')
        return render(request, 'elver/api/api_task_content_result.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def task_report_page(cls, request,*arg,**kwargs):
        """自动化报告页"""
        taskname = kwargs['taskname']
        run_id = kwargs['run_id']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        report_num = models.AutomationTaskResult.objects.filter(taskname=taskname,run_id=run_id).count()
        if report_num > 0:
            run_ids = models.AutomationTaskResult.objects.filter(taskname=taskname).values('run_id').distinct()
            runner = models.AutomationTaskResult.objects.filter(taskname=taskname,run_id=run_id).values("runner").first()['runner']
            ctime = models.AutomationTaskResult.objects.filter(taskname=taskname,run_id=run_id).values("ctime").first()['ctime']
            results = models.AutomationTaskResult.objects.filter(taskname=taskname,run_id=run_id).order_by('-id')
            success_num = models.AutomationTaskResult.objects.filter(taskname=taskname,run_id=run_id,status='成功').count()
            fail_num = report_num - success_num
        return render(request, 'elver/api/api_task_report.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
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
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        cases = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname).order_by('id')
        case_num = models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname).count()
        if case_num > 0:
            casename = kwargs['casename']
            case_type = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).values("case_type").first()['case_type']
            case_id = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).values("id").first()['id']
            if case_type in ['Json','Get']:
                request_content = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).values("request_content").first()['request_content']
            else:
                request_content = '{}'
            try:    
                script_name = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).values("request_content").first()['request_content']
                script_file = open(cls.script_dir + script_name, "r")
                script_content = script_file.read()
            except Exception as e:
                print(str(e))   
            case_asserts = models.AutomationTaskCaseAssert.objects.filter(taskname=taskname,apiname=apiname,casename=casename).order_by('id')
        return render(request, 'elver/api/api_case.html', locals())

    @classmethod
    @method_decorator(Decorators.catch_except)
    def create_task_api(cls, request):
        """创建任务接口"""
        taskname = common.request_method(request, "taskname")
        owner = common.request_method(request, "owner")
        task_num = models.AutomationTask.objects.filter(taskname=taskname).count()
        if task_num == 0:
            models.AutomationTask(taskname=taskname,owner=owner,task_user=owner).save()
            avatar = models.User.objects.filter(username=owner).values("avatar").first()['avatar']
            models.AutomationTaskUser(taskname=taskname, username=owner, role='管理员', avatar=avatar).save()
            result = {'status': 1, 'msg': '创建任务成功'}
        else:
            result = {'status': 0, 'msg': '该任务已存在'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
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
    @method_decorator(Decorators.catch_except)
    def edit_task_api(cls, request):
        """编辑任务信息接口"""
        taskname = common.request_method(request,"taskname")
        new_taskname = common.request_method(request,"new_taskname")
        timer_switch = common.request_method(request, "timer_switch")
        timer_value = common.request_method(request, "timer_value")
        ding_switch = common.request_method(request, "ding_switch")
        ding_token = common.request_method(request, "ding_token")
        try:
            models.AutomationTask.objects.filter(taskname=taskname).update(timer_value=timer_value, timer_switch=timer_switch,
                                                                           ding_token=ding_token,ding_switch=ding_switch)
            if taskname != new_taskname:
                task_num = models.AutomationTask.objects.filter(taskname=new_taskname).count()
                if task_num == 0 :
                    models.AutomationTask.objects.filter(taskname=taskname).update(taskname=new_taskname)
                    models.AutomationTaskContent.objects.filter(taskname=taskname).update(taskname=new_taskname)
                    models.AutomationTaskCase.objects.filter(taskname=taskname).update(taskname=new_taskname)
                    models.AutomationTaskCaseAssert.objects.filter(taskname=taskname).update(taskname=new_taskname)
                    models.AutomationTaskResult.objects.filter(taskname=taskname).update(taskname=new_taskname)
                    result = {'status': 1, 'msg': '更新成功！'}
                else:
                    result = {'status': 0, 'msg': '该任务名称已经被使用'}
            else:
                result = {'status': 1, 'msg': '更新成功！'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
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
    @method_decorator(Decorators.catch_except)
    def run_task_api(cls, request):
        """执行任务接口"""
        taskname = common.request_method(request, "taskname")
        new_status = common.request_method(request, "new_status")
        try:
            models.AutomationTask.objects.filter(taskname=taskname).update(status=new_status)
            result = {'status': 1, 'msg': '开始执行！'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def delete_task_api(cls, request):
        """删除任务接口"""
        taskname = common.request_method(request, "taskname")
        owner = common.request_method(request, "owner")
        task_owner = models.AutomationTask.objects.filter(taskname=taskname).values("owner").last()['owner']
        api_num = models.AutomationTaskContent.objects.filter(taskname=taskname).count()
        if owner == task_owner and api_num == 0:
            models.AutomationTask.objects.filter(taskname=taskname).delete()
            models.AutomationTaskUser.objects.filter(taskname=taskname).delete()
            result = {'status': 1, 'msg': '删除成功！'}
        else:
            if owner != task_owner:
                result = {'status': 0, 'msg': '不是OWNER,无法操作!'}
            else:
                result = {'status': 0, 'msg': '该任务下有接口数>0'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def create_task_content_api(cls, request):
        """创建任务内容接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        url = common.request_method(request, "url")
        username = request.session['username']
        if apiname and url:
            if str(url).startswith('http'):
                api_num = models.AutomationTaskContent.objects.filter(taskname=taskname,apiname=apiname).count()
                if api_num == 0:
                    apiname = apiname.replace('/','_').replace(' ','')
                    models.AutomationTaskContent(taskname=taskname, apiname=apiname,url=url).save()
                    sum_num = models.AutomationTaskContent.objects.filter(taskname=taskname).count()
                    models.AutomationTask.objects.filter(taskname=taskname).update(sum_num=sum_num)
                    result = {'status': 1, 'msg': '创建接口成功'}

                else:
                    result = {'status': 0, 'msg': '该接口已存在'}
            else:
                result = {'status': 0, 'msg': '接口URL开头不是http'}        
        else:
            result = {'status': 0, 'msg': '接口名称和地址不能为空'}       
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def edit_task_content_api(cls, request):
        """编辑任务内容接口"""
        id = common.request_method(request, "id")
        old_apiname = models.AutomationTaskContent.objects.filter(id=id).values("apiname").first()['apiname']
        new_apiname = common.request_method(request, "new_apiname")
        new_url = common.request_method(request, "new_url")
        username = request.session['username']
        ctime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        #todo:更改apiname要同步修改用例和断言表
        try:
            if str(new_url).startswith('http'):
                if new_apiname:
                    new_apiname = new_apiname.replace('/','_').replace(' ','')
                    models.AutomationTaskContent.objects.filter(id=id).update(apiname=new_apiname, url=new_url,ctime=ctime)
                    models.AutomationTaskCase.objects.filter(apiname=old_apiname).update(apiname=new_apiname)
                    models.AutomationTaskCaseAssert.objects.filter(apiname=old_apiname).update(apiname=new_apiname)
                    result = {'status': 1, 'msg': '更新成功！'}
                else:
                    result = {'status': 0, 'msg': '接口名称不能为空'}   
            else:
                result = {'status': 0, 'msg': '接口URL开头不是http'}       
        except Exception as e:
            result = {'status': 0, 'msg':str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def get_online_apiname_api(cls, request):
        """获取任务所有在线内容接口"""
        taskname = common.request_method(request, "taskname")
        if taskname:
            apiinfos = models.AutomationTaskContent.objects.filter(Q(taskname=taskname) & ~Q(status='下线'))
            apidata_list = [apiinfo.apiname for apiinfo in apiinfos]
            result = {'status': 1, 'msg': 'success', 'data': apidata_list}
        else:
            result = {'status': 0, 'msg': 'taskname is empty'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def get_timer_task_api(cls, request):
        """获取所有定时任务"""
        timer_value = common.request_method(request, "timer_value")
        tasknames = models.AutomationTask.objects.filter(timer_switch='true',timer_value=timer_value).values('taskname').distinct()
        taskname_list = [taskname['taskname'] for taskname in tasknames]
        if len(taskname_list) > 0:
            result = {'status': 1, 'msg': 'success', 'data': taskname_list}
        else:
            result = {'status': 0, 'msg': 'taskname is empty'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def set_apiname_status_api(cls, request):
        """更新任务api状态接口"""
        taskname = common.request_method(request, "taskname")
        new_status = common.request_method(request, "new_status")
        ctime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        try:
            apiinfos = models.AutomationTaskContent.objects.filter(Q(taskname=taskname) & ~Q(status='下线'))
            apidata_list = [apiinfo.apiname for apiinfo in apiinfos]
            print(apidata_list)
            for i in range(len(apidata_list)):
                models.AutomationTaskContent.objects.filter(taskname=taskname,apiname=apidata_list[i]).update(status=new_status,ctime=ctime)
            models.AutomationTask.objects.filter(taskname=taskname).update(status=new_status)
            result = {'status': 1, 'msg': '更新成功！'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def run_jenkins_job_api(cls, request):
        """执行jenkins任务-run_task_all_apiname"""
        jobname = common.request_method(request, "jobname")
        taskname = common.request_method(request, "taskname")
        owner = common.request_method(request, "owner")
        run_id = common.request_method(request, "run_id")
        parameter = {'taskname':taskname,'owner':owner,'run_id':run_id}
        try:
            common.build_jenkins_job(jobname=jobname, parameter=parameter)
            result = {'status': 1, 'msg': 'success'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def run_task_content_api(cls, request):
        """执行任务用例接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        owner = common.request_method(request, "owner")
        run_id = common.request_method(request, "run_id")
        case_num = models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname).count()
        ding_token = models.AutomationTask.objects.filter(taskname=taskname).values("ding_token").first()['ding_token']
        ding_switch = models.AutomationTask.objects.filter(taskname=taskname).values("ding_switch").first()['ding_switch']
        ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if case_num > 0:
            try:
                status_flage = '成功'
                url = \
                models.AutomationTaskContent.objects.filter(taskname=taskname, apiname=apiname).values("url").first()['url']

                case_datas = models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname)
                case_dict_list = [
                    {
                        'request_content': case_data.request_content,
                        'case_type': case_data.case_type,
                        'casename': case_data.casename
                    }
                    for case_data in case_datas
                ]

                for i in range(len(case_dict_list)):
                    # code参数校验
                    if case_dict_list[i]['case_type'] in ['Get', 'Json']:
                        request_content = case_dict_list[i]['request_content']
                    else:
                        script_content = \
                            models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname,
                                                                     casename=case_dict_list[i]['casename']).values(
                                "request_content").first()['request_content']
                        script_result = common.putcmd(f'python3 {cls.script_dir}{script_content}')
                        request_content = script_result[0]

                    code_result_data = common.assert_check(check_type='code', case_type=case_dict_list[i]['case_type'],
                                                           url=url,
                                                           playload=request_content,
                                                           parameter='code',
                                                           assert_type='==', value='200')
                    status = ('失败', '成功')[code_result_data['pass']]
                    if code_result_data['pass'] is False:
                        status_flage = '失败'
                        common.send_api_error_msg(taskname=taskname, apiname=apiname, url=url,ding_switch=ding_switch,
                                                  casename=case_dict_list[i]['casename'],
                                                  request_content=request_content, response='none', parameter='code',
                                                  pre_value='200', assert_type='==',
                                                  final_value=code_result_data['final'],
                                                  dingding_robot_token=ding_token,run_id=run_id)

                    models.AutomationTaskResult(taskname=taskname, apiname=apiname,
                                                casename=case_dict_list[i]['casename'],
                                                parameter='code', assert_type='==', pre_value='200',
                                                final_value=code_result_data['final'],
                                                runner=owner, status=status, response=code_result_data['response'],
                                                ctime=ctime, run_id=run_id).save()
                    # 其他参数校验
                    assert_datas = models.AutomationTaskCaseAssert.objects.filter(taskname=taskname,apiname=apiname,
                                                                                  casename=case_dict_list[i]['casename'])

                    assert_dict_list = [
                        {
                            'casename': assert_data.casename,
                            'parameter': assert_data.parameter,
                            'value': assert_data.value,
                            'assert_type': assert_data.assert_type
                        }
                        for assert_data in assert_datas
                    ]

                    for j in range(len(assert_dict_list)):
                        try:
                            other_result_data = common.assert_check(check_type='other',
                                                                case_type=case_dict_list[i]['case_type'],
                                                                url=url, playload=request_content,
                                                                parameter=assert_dict_list[j]['parameter'],
                                                                assert_type=assert_dict_list[j]['assert_type'],
                                                                value=assert_dict_list[j]['value'])

                            status = ('失败', '成功')[other_result_data['pass']]
                            if other_result_data['pass'] is False:
                                status_flage = '失败'
                                common.send_api_error_msg(taskname=taskname, apiname=apiname, url=url,ding_switch=ding_switch,
                                                          casename=assert_dict_list[j]['casename'],
                                                          request_content=request_content, response=other_result_data['response'],
                                                          parameter=assert_dict_list[j]['parameter'],
                                                          pre_value=assert_dict_list[j]['value'], assert_type=assert_dict_list[j]['assert_type'],
                                                          final_value=other_result_data['final'],
                                                          dingding_robot_token=ding_token,run_id=run_id)

                            models.AutomationTaskResult(taskname=taskname, apiname=apiname,
                                                        casename=assert_dict_list[j]['casename'],
                                                        parameter=assert_dict_list[j]['parameter'],
                                                        assert_type=assert_dict_list[j]['assert_type'],
                                                        pre_value=assert_dict_list[j]['value'],
                                                        final_value=other_result_data['final'],
                                                        runner=owner, status=status,
                                                        response=other_result_data['response'],
                                                        ctime=ctime, run_id=run_id).save()

                        except Exception as e:
                            status_flage = '失败'
                            common.send_api_error_msg(taskname=taskname, apiname=apiname, url=url,ding_switch=ding_switch,
                                                      casename=assert_dict_list[j]['casename'],
                                                      request_content=request_content,
                                                      response=f'用例异常:{str(e)}',
                                                      parameter=assert_dict_list[j]['parameter'],
                                                      pre_value=assert_dict_list[j]['value'],
                                                      assert_type=assert_dict_list[j]['assert_type'],
                                                      final_value=f'用例异常:{str(e)}',
                                                      dingding_robot_token=ding_token,run_id=run_id)

                            models.AutomationTaskResult(taskname=taskname, apiname=apiname,
                                                        casename=assert_dict_list[j]['casename'],
                                                        parameter=assert_dict_list[j]['parameter'],
                                                        assert_type=assert_dict_list[j]['assert_type'],
                                                        pre_value=assert_dict_list[j]['value'],
                                                        final_value='none',
                                                        runner=owner, status=status_flage,
                                                        response='none',
                                                        ctime=ctime, run_id=run_id,error=str(e)).save()

                models.AutomationTaskContent.objects.filter(taskname=taskname,apiname=apiname).update(status=status_flage, ctime=ctime,run_id=run_id)

                result = {'status': 1, 'msg': 'success','result':status_flage}

            except Exception as e:
                result = {'status': 0, 'msg': f'{apiname}执行异常：{str(e)}'}
        else:
            result = {'status': 0, 'msg': f'{apiname}没有用例'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def delete_task_content_api(cls, request):
        """删除任务api接口"""
        id = common.request_method(request, "id")
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        models.AutomationTaskContent.objects.filter(id=id).delete()
        models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname).delete()
        models.AutomationTaskCaseAssert.objects.filter(taskname=taskname,apiname=apiname).delete()
        sum_num = models.AutomationTaskContent.objects.filter(taskname=taskname).count()
        models.AutomationTask.objects.filter(taskname=taskname).update(sum_num=sum_num)
        result = {'status': 1, 'msg': '删除成功！'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def create_task_case_api(cls, request):
        """创建任务用例接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        case_type = common.request_method(request, "case_type")
        casename = common.request_method(request, "casename")
        username = request.session['username']
        ctime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        try:
            case_num = models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname,casename=casename).count()
            if case_num == 0:
                if case_type == 'Script':
                    models.AutomationTaskCase(taskname=taskname, apiname=apiname, case_type=case_type,
                    casename=casename,request_content=str(ctime)+'.py').save()
                    fp = open(cls.script_dir+str(ctime)+'.py','w')
                    fp.close()
                elif case_type == 'Json':
                    models.AutomationTaskCase(taskname=taskname, apiname=apiname, case_type=case_type,casename=casename,request_content='{}').save()
                else:
                    models.AutomationTaskCase(taskname=taskname, apiname=apiname, case_type=case_type,casename=casename).save()

                result = {'status': 1, 'msg': '创建用例成功'}
            else:
                result = {'status': 0, 'msg': '该用例名称已存在'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def edit_task_case_api(cls, request):
        """编辑任务用例接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        case_type = common.request_method(request, "case_type")
        casename = common.request_method(request, "casename")
        request_content = common.request_method(request, "request_content")
        try:
            if case_type in ['Json','Get']:
                models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname, casename=casename).update(request_content=request_content)
            else:
                script_name = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).values("request_content").first()['request_content']
                fp = open(cls.script_dir+script_name,'w')
                fp.write(request_content)
                fp.close()    
            result = {'status': 1, 'msg': '保存成功！'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def edit_case_assert_api(cls, request):
        """编辑用例断言接口"""
        assert_id = common.request_method(request, "assert_id")
        parameter = common.request_method(request, "parameter")
        value = common.request_method(request, "value")
        assert_type = common.request_method(request, "assert_type")
        try:
            models.AutomationTaskCaseAssert.objects.filter(assert_id=assert_id).update(parameter=parameter,value=value,assert_type=assert_type)
            result = {'status': 1, 'msg': '保存成功！'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def delete_task_case_api(cls, request):
        """删除任务用例接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        casename = common.request_method(request, "casename")
        models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).delete()
        models.AutomationTaskCaseAssert.objects.filter(taskname=taskname,apiname=apiname,casename=casename).delete()
        case_num = models.AutomationTaskCase.objects.filter(taskname=taskname, apiname=apiname).count()
        if case_num > 0:
            first_casename = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname).values("casename").first()['casename']
            result = {'status': 1, 'msg': '删除成功！','first_casename':first_casename}
        else:
            result = {'status': 1, 'msg': '删除成功！', 'first_casename': 'no case'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    @classmethod
    @method_decorator(Decorators.catch_except)
    def create_case_assert_api(cls, request):
        """创建用例断言接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        casename = common.request_method(request, "casename")
        parameter = common.request_method(request, "parameter")
        value = common.request_method(request, "value")
        assert_type = common.request_method(request, "assert_type")
        active_id = common.request_method(request, "active_id")
        assert_id = f'assert_{active_id}'
        assert_type_id = f'assert_type_{active_id}'
        parameter_id = f'parameter_{active_id}'
        value_id = f'value_{active_id}'
        debug_id = f'debug_{active_id}'
        del_id = f'del_{active_id}'
        try:
            models.AutomationTaskCaseAssert(taskname=taskname, apiname=apiname,casename=casename,
            assert_type=assert_type,parameter=parameter,value=value,assert_type_id=assert_type_id,
            assert_id=assert_id,parameter_id=parameter_id,value_id=value_id,debug_id=debug_id,del_id=del_id).save()
            result = {'status': 1, 'msg': '创建断言成功'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    @classmethod
    @method_decorator(Decorators.catch_except)
    def delete_case_assert_api(cls, request):
        """删除用例断言接口"""
        assert_id = common.request_method(request, "assert_id")
        try:
            models.AutomationTaskCaseAssert.objects.filter(assert_id=assert_id).delete()
            result = {'status': 1, 'msg': '删除成功！'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}    
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def debug_case_assert_api(cls, request):
        """调试用例断言接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        casename = common.request_method(request, "casename")
        url = models.AutomationTaskContent.objects.filter(taskname=taskname,apiname=apiname).values("url").first()['url']
        case_type = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).values("case_type").first()['case_type']
        parameter = common.request_method(request, "parameter")
        assert_type = common.request_method(request, "assert_type")
        value = common.request_method(request, "value")
        check_type = common.request_method(request, "check_type")
        if case_type in ['Get','Json']:
            request_content = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).values("request_content").first()['request_content']
        else:
            script_content = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).values("request_content").first()['request_content']
            script_result = common.putcmd(f'python3 {cls.script_dir}{script_content}')
            if script_result[1]:
                result = {'status': 0, 'msg': script_result[1]}
                return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                request_content = script_result[0]
        try:
            debug_data = common.assert_check(check_type=check_type,case_type=case_type,url=url,playload=request_content
            ,parameter=parameter,assert_type=assert_type,value=value)
            result = {'status': 1, 'msg': '调试通过！','data':debug_data}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}    
        return HttpResponse(json.dumps(result), content_type="application/json")    
    
    @classmethod
    @method_decorator(Decorators.catch_except)
    def debug_case_script_api(cls, request):
        """调试用例脚本接口"""
        taskname = common.request_method(request, "taskname")
        apiname = common.request_method(request, "apiname")
        casename = common.request_method(request, "casename")
        script_name = models.AutomationTaskCase.objects.filter(taskname=taskname,apiname=apiname,casename=casename).values("request_content").first()['request_content']
        try:
            script_result = common.putcmd(f'python3 {cls.script_dir}{script_name}')
            if script_result[1]:
                result = {'status': 0, 'msg': script_result[1]}
            else:
                result = {'status': 1, 'msg': '调试通过！','data':script_result[0]}    
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}    
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def add_task_user_api(cls, request):
        """添加任务成员接口"""
        taskname = common.request_method(request, "taskname")
        username = common.request_method(request, "username")
        owner = common.request_method(request, "owner")
        role = models.AutomationTaskUser.objects.filter(taskname=taskname,username=owner).values("role").first()['role']
        try:
            if role == '管理员':
                user_num = models.AutomationTaskUser.objects.filter(taskname=taskname, username=username).count()
                if user_num > 0:
                    result = {'status': 0, 'msg': '该成员已存在'}
                else:
                    avatar = models.User.objects.filter(username=username).values("avatar").first()['avatar']
                    models.AutomationTaskUser(taskname=taskname,username=username,role='成员',avatar=avatar).save()
                    old_task_user = \
                    models.AutomationTask.objects.filter(taskname=taskname).values("task_user").first()[
                        'task_user']
                    new_task_user = old_task_user+';'+username
                    models.AutomationTask.objects.filter(taskname=taskname).update(task_user=new_task_user)
                    result = {'status': 1, 'msg': '添加成功'}
            else:
                result = {'status': 0, 'msg': '不是管理员，没有权限'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def remove_task_user_api(cls, request):
        """移除任务成员接口"""
        taskname = common.request_method(request, "taskname")
        username = common.request_method(request, "username")
        owner = common.request_method(request, "owner")
        role = models.AutomationTaskUser.objects.filter(taskname=taskname,username=owner).values("role").first()['role']
        try:
            if role == '管理员':
                models.AutomationTaskUser.objects.filter(taskname=taskname,username=username).delete()
                old_task_user = \
                    models.AutomationTask.objects.filter(taskname=taskname).values("task_user").first()[
                        'task_user']
                new_task_user = old_task_user.replace(f';{username}','')
                models.AutomationTask.objects.filter(taskname=taskname).update(task_user=new_task_user)
                result = {'status': 1, 'msg': '删除成功'}
            else:
                result = {'status': 0, 'msg': '不是管理员，没有权限'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

class API_STRESS_TEST(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def stress_test_page(cls,request):
        """压力测试主页"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        task_num = models.StressTestTask.objects.all().count()
        tasks = models.StressTestTask.objects.all().order_by('-id')
        task_names = models.StressTestTask.objects.all().values('taskname').distinct()
        return render(request, 'elver/api/api_stress_test.html',locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def create_plan_page(cls, request):
        """创建测试计划页面"""
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        task_num = models.StressTestTask.objects.all().count()
        tasks = models.StressTestTask.objects.all().order_by('-id')
        task_names = models.StressTestTask.objects.all().values('taskname').distinct()
        return render(request, 'elver/api/api_stress_plan.html', locals())