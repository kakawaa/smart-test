# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from functools import wraps
import json
from django.contrib import auth
from django.db.models import Q
from testsite import models
from testsite.Common import commonFunc
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import datetime,time
import os
import requests
import psutil
from crontab import CronTab
import unittest
import sys
import os
import traceback
import time
import MySQLdb
import sys
import base64
import hashlib
import hmac
from jira import JIRA
sys.getdefaultencoding()

def add_log(username,opration,api):
    models.operation_log.objects.create(date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                        user=username, operation=opration,
                                        api=api)
# def page_404(request,exception, template_name='404.html'):
#     return render(request, template_name)
def page_404(request):
    return render(request, 'quickit/404.html')

def login_page(request):
    return render(request, 'quickit/login.html')

def tool(request):
    return render(request, 'quickit/tool.html')

def bug_monitor(request):
    return render(request, 'quickit/bug_monitor.html')

def MasterList(request):
    return render(request, 'quickit/MasterList.html')

def ding_build_apk(request):
    anm = request.GET.get("anm")
    env = request.GET.get("env")
    nickname = request.GET.get('nickname')
    add_log(nickname,'钉钉打包','ding_build_apk')
    data = models.ding_build_apk.objects.filter(anm=anm, env=env)
    if data:
        jobname = data.values("jobname").first()['jobname']
        parameters = data.values("parameters").first()['parameters']
        result = {"status":200,"data":{'anm': anm, 'env': env, "jobname": jobname, "parameters": parameters}}
    else:
        result = {"status":404,"data":{}}
    return HttpResponse(json.dumps(result), content_type="application/json")


def scan_login(request):
    #修改为后端请求钉钉url
    ding_url = request.POST.get('ding_url')
    result = requests.get(ding_url)
    request.session['is_login'] = '1'
    request.session['username'] = result.json()['username']
    request.session['nickname'] = result.json()['nickname']
    return HttpResponse(json.dumps(result.json()), content_type="application/json")

def scan_login_api(request):
    if request.method == "GET":
        ##########二维码认证登录#############
        code = request.GET.get('code', )
        # 正式的appid
        appId = 'dingoamin5ak8wdta8eqh6'
        appSecret = 'B_r1uD7PLZ7zJxBfLBRIbw46yHe1SvW4XhGeoJti0Lgppu_mF2SIEHb_DLXhzNME'

        # 测试的appid
        # appId = 'dingoasxmgpylvxyriweyo'
        # appSecret = '4M0yE9RtN_gFqzGQp9_9XguyFSyDqRkd9Vj1ED86lLtLhDmuEa0YlccoPQizVqS4'

        # 获取token
        token = requests.get(
            'https://oapi.dingtalk.com/sns/gettoken?appid={appId}&appsecret={appSecret}'.format(appId=appId,
                                                                                                appSecret=appSecret))
        access_token = token.json()["access_token"]

        tmp_auth_code = requests.post(
            "https://oapi.dingtalk.com/sns/get_persistent_code?access_token={access_token}".format(
                access_token=access_token),
            json={
                "tmp_auth_code": code
            })

        tmp_code = tmp_auth_code.json()
        openid = tmp_code['openid']
        persistent_code = tmp_code['persistent_code']
        sns_token_request = requests.post(
            "https://oapi.dingtalk.com/sns/get_sns_token?access_token={access_token}".format(access_token=access_token),
            json={
                "openid": openid,
                "persistent_code": persistent_code
            })
        sns_token = sns_token_request.json()['sns_token']
        user_info_request = requests.get(
            'https://oapi.dingtalk.com/sns/getuserinfo?sns_token={sns_token}'.format(sns_token=sns_token))
        user_info = user_info_request.json()['user_info']
        username = user_info['nick']
        # 新应用获取token，并通过unionid获取userid
        appid_new = 'dingoittvgrts0o0f7cc'
        appSecret_new = 'VRB-41x71uYcwOtKi7r8YSj-Xro0kRLLywjdD5Rxc5Cgx6SeNME80j5WhYjlVdMh'
        user_token = requests.get(
            'https://oapi.dingtalk.com/gettoken?corpid={corpid}&corpsecret={corpsecret}'.format(corpid=appid_new,
                                                                                                    corpsecret=appSecret_new))
        user_id_reponse = requests.get(
            'https://oapi.dingtalk.com/user/getUseridByUnionid?access_token={user_token}&unionid={unionid}'.format(user_token=user_token.json()['access_token'],
                                                                                                unionid=user_info['unionid']))
        errcode = user_id_reponse.json()['errcode']
        # errcode=0代表用户存在
        if errcode == 0:
            user = models.User.objects.filter(username=username)
            if not user:
                insert_user = models.User(username=username, password='dfajSUmLT#y#iOT8r6%20pk&',super_admin=0, nickname=username,
                                          admin_type=0,anm='')
                insert_user.save()
            result = {'code': 200, 'msg': 'login suc!','nickname':username,'username':username}
        else:
            result = {'code': 202, 'msg': 'login wrong!','nickname':'','username':''}
    return HttpResponse(json.dumps(result), content_type="application/json")


def login_api(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    else:
        username = request.GET.get('username')
        password = request.GET.get('password')
    user = models.User.objects.filter(username=username, password=password)
    if user:
        # 登录成功
        # 1，生成特殊字符串
        # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
        # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
        request.session['is_login'] = '1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
        request.session['username'] = username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
        nickname = models.User.objects.filter(username=username, password=password).values("nickname").first()[
            'nickname']
        if nickname == '':
            nickname = username
        request.session['nickname'] = nickname
        add_log(username, '登录成功', 'login_api')

        # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
        result = {'code': 200, 'msg': 'old password wrong!'}
    else:
        # message = '帐户或密码错误！！'
        # return render(request, 'quickit/login_old.html', {'message': message})
        result = {'code': 202, 'msg': 'old password wrong!'}
        add_log(username, '登录失败，账号：%s,密码：%s' % (username, password), 'login_api')

    return HttpResponse(json.dumps(result), content_type="application/json")


def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login/')
    return inner

@check_login
def logout(request):
    username = request.session['username']
    add_log(username, '退出登录', 'login_api')
    auth.logout(request)
    response = redirect('/login/')
    return response

@check_login
def apk(request):
    """
    apk列表页面
    """
    username = request.session['username']
    add_log(username, '进入apk list页面', 'apk')
    nickname = request.session['nickname']

    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    apk_infos = models.Apk.objects.all().order_by('-id')[:500]
    package_names = models.Apk.objects.values('package_name').distinct()
    app_list = []
    for package_name in package_names:
        app_list.append(package_name['package_name'])
    return render(request, 'quickit/apk_list.html', locals()) #locals()函数会以字典类型返回当前位置的全部局部变量

@check_login
def detail(request, apk_name):
    """
    apk包详情页面
    """
    username = request.session['username']
    add_log(username, '进入apk详情页，apk=%s'%apk_name, 'detail')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']

    apk_info = get_object_or_404(models.Apk, apk_name=apk_name)
    apk_detail = get_object_or_404(models.Size, apk_name=apk_name)
    return render(request, 'quickit/detail.html', locals())


@check_login
def ad_sample(request):
    """
    广告抽样
    """
    username = request.session['username']
    add_log(username, '进入广告抽样页', 'ad_sample')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']

    ad_sources = models.Ad_sample_stat.objects.values('source_name').distinct()
    ad_source_list = []
    for ad_source in ad_sources:
        ad_source_list.append(ad_source['source_name'])
    return render(request, 'quickit/ad_sample.html', locals())

@check_login
def ad_sample_report(request):
    username = request.session['username']
    add_log(username, '查看抽样报告', 'ad_sample_report')

    ad_source_list = request.POST.get("ad_source_list").split(",")
    loc_list = request.POST.get("loc_list").split(",")
    ad_size_list = request.POST.get("ad_size_list").split(",")
    date = request.POST.get("date").replace(' ','').split("-")
    start_year = int(date[0].split("/")[0])
    start_month = int(date[0].split("/")[1])
    start_day = int(date[0].split("/")[2])

    end_year = int(date[1].split("/")[0])
    end_month = int(date[1].split("/")[1])
    end_day = int(date[1].split("/")[2])

    if 'All' in ad_source_list or ad_source_list==['']:
        ad_sources = models.Ad_sample_stat.objects.values('source_name').distinct()
        ad_source_list = []
        for source in ad_sources:
            ad_source_list.append(source['source_name'])

    if 'All' in loc_list or loc_list == ['']:
        loc_list = ['EGY','IRQ','DZA','IDN','IND','MMR','PHL','NPL','BGD','PAK']

    if 'All' in ad_size_list or ad_size_list == ['']:
        ad_size_list = ['banner_300_250','banner_320_100','native_320_480','native_1200_627']

    all_response = {}
    table_data_list = []

    image_data_list = []
    image_data = {}
    for ad_source in ad_source_list:
        '''遍历选中的广告源'''
        ad_source_data = {}
        for loc in loc_list:
            loc_data_list = []
            '''遍历选中的地区'''
            stat = models.Ad_sample_stat.objects.filter(loc=loc,source_name=ad_source,dt__gte=datetime.date(start_year,start_month,start_day),dt__lte=datetime.date(end_year,end_month,end_day))
            for i in stat:
                table_data = []
                table_data.append(str(i.dt))
                table_data.append(i.source_name)
                table_data.append(i.loc)
                table_data.append(i.req)
                table_data.append(i.suc)
                table_data.append(i.fail)
                table_data_list.append(table_data)

            for ad_size in ad_size_list:
                info = models.Ad_sample_info.objects.filter(country=loc,source_name=ad_source,ad_size=ad_size,dt__gte=datetime.date(start_year,start_month,start_day),dt__lte=datetime.date(end_year,end_month,end_day))
                for j in info:
                    loc_data = {}
                    loc_data['source_name'] = j.source_name
                    loc_data['country'] = j.country
                    loc_data['title'] = j.title
                    loc_data['desc_str'] = j.desc_str
                    loc_data['image_url'] = j.image_url
                    loc_data['click_url'] = j.click_url
                    loc_data['request_time'] = str(j.request_time)
                    loc_data['is_html'] = j.is_html
                    loc_data['html_str'] = j.html_str
                    loc_data['creative_id'] = j.creative_id
                    loc_data['ad_size'] = j.ad_size
                    loc_data_list.append(loc_data)
            if loc_data_list!=[]:
                ad_source_data[loc] = loc_data_list

        if ad_source_data !={}:
            image_data[ad_source] = ad_source_data
    image_data_list.append(image_data)
    all_response['stat'] = table_data_list
    all_response['info'] = image_data_list
    return HttpResponse(json.dumps(all_response), content_type="application/json")

@check_login
def dashboard(request):
    """
    dashboard页面
    """


    nickname = request.session['nickname']
    username = request.session['username']
    add_log(username, '进入dashboard页面', 'dashboard')
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    # admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    # print(admin_type)
    return render(request, 'quickit/dashboard.html', locals())

@check_login
def api_test(request):
    """
    api测试页面
    """
    username = request.session['username']
    add_log(username, '进入api测试页面', 'api_test')
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']

    Task_infos = models.APItask.objects.all().order_by('-id')
    nickname = request.session['nickname']
    projects = models.APItask.objects.values('project').distinct()
    project_list = []
    for project in projects:
        project_list.append(project['project'])
    return render(request, 'quickit/api_test.html', locals())

@check_login
def test_result(request):
    """
    Task测试结果页面
    """
    test_result_infos = models.Taskresult.objects.all().order_by('-id')
    username = request.session['username']
    add_log(username, '进入Task测试结果页面', 'test_result')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']


    Result_infos = models.Taskresult.objects.all().order_by('-id')
    projects = models.Taskresult.objects.values('project').distinct()
    project_list = []
    for project in projects:
        project_list.append(project['project'])
    return render(request, 'quickit/test_result.html', locals())

def test_result_api(request):
    """
    测试结果查询接口
    """
    username = request.session['username']
    add_log(username, 'api测试结果查询', 'test_result_api')
    project = request.POST.get("project")
    filter = request.POST.get("filter")
    keyword = request.POST.get("keyword")
    rerult_flag = request.POST.get("rerult_flag")
    # 给test maker调用
    env = request.POST.get("env")
    taskname = request.POST.get("taskname")

    if rerult_flag:
        test_result_content = \
        models.Taskresult.objects.filter(project=project, env=env, taskname=taskname).values("result").first()['result']

    else:
        test_result_content='NA'
    if project == 'All':
        if keyword == "":
            data = models.Taskresult.objects.all().order_by('-id')[:100]
        elif keyword != '':
            if filter == 'Env':
                data = models.Taskresult.objects.filter(env =  keyword).order_by('-id')[:100]
            elif filter == 'Task':
                data = models.Taskresult.objects.filter(taskname= keyword).order_by('-id')[:100]
    elif project != 'All':
        if keyword == "":
            data = models.Taskresult.objects.filter(project=project).order_by('-id')[:100]
        elif keyword != '':
            if filter == 'Env':
                data = models.Taskresult.objects.filter(project=project,env= keyword).order_by('-id')[:100]
            elif filter == 'Task':
                data = models.Taskresult.objects.filter(project=project,taskname= keyword).order_by('-id')[:100]
    resultdata_list = []
    for result in data:
        resultdata = []
        resultdata.append(result.id)
        resultdata.append(result.project)
        resultdata.append(result.env)
        resultdata.append(result.taskname)
        resultdata.append(result.status)
        resultdata.append(str(result.ctime))
        resultdata_list.append(resultdata)
    result = {'code': 200, 'msg': 'success','resultdata':resultdata_list,'testresult':test_result_content}

    return HttpResponse(json.dumps(result), content_type="application/json")


@check_login
def report(request,taskname):
    """
    测试报告页面
    """
    username = request.session['username']
    add_log(username, '进入测试报告页面report', 'report')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']

    taskname = str(taskname).strip()
    testresult =  models.Taskresult.objects.filter(taskname=taskname).values("result").last()['result']
    errorcount = models.Taskresult.objects.filter(taskname=taskname).values("errorcount").last()['errorcount']
    passcount = models.Taskresult.objects.filter(taskname=taskname).values("passcount").last()['passcount']

    return render(request, 'quickit/report.html', locals())

@check_login
def test_report(request,id):
    """
    测试报告页面
    """
    username = request.session['username']
    add_log(username, '进入测试报告页面test_report', 'test_report')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']

    id = id
    testresult =  str(models.Taskresult.objects.filter(id=id).values("result").last()['result']).replace("False","\'false\'").replace("True","\'true\'").replace("None","\'None\'")
    errorcount = models.Taskresult.objects.filter(id=id).values("errorcount").last()['errorcount']
    passcount = models.Taskresult.objects.filter(id=id).values("passcount").last()['passcount']

    return render(request, 'quickit/report.html', locals())

@check_login
def apm_online(request):
    """
    apm线上监控页面
    """
    username = request.session['username']
    add_log(username, '进入apm线上监控页面', 'apm_online')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']

    return render(request, 'quickit/apm_online.html', locals())

@check_login
def apm_offline(request):
    """
    apm线下监控页面
    """
    username = request.session['username']
    add_log(username, '进入apm线下监控页面', 'apm_offline')

    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    StartUpTime_infos = models.StartUpTime.objects.filter(~Q(status='Delete')).order_by('-id')
    Performance_infos = models.Performance.objects.all().order_by('-id')
    package_names = models.StartUpTime.objects.values('pkgname').distinct()
    compare_projects = models.StartUpTime.objects.filter(status='Competitor').values('pkgname').distinct()
    TimeCost_scenes = models.StartUpTime.objects.values('scene').distinct()
    Performance_scenes = models.Performance.objects.values('scene').distinct()
    app_list = []
    compare_project_list=[]
    timecost_scene_list=[]
    performance_scene_list=[]
    for package_name in package_names:
        app_list.append(package_name['pkgname'])
    for compare_project in compare_projects:
        compare_project_list.append(compare_project['pkgname'])
    for TimeCost_scene in TimeCost_scenes:
        timecost_scene_list.append(TimeCost_scene['scene'])
    for Performance_scene in Performance_scenes:
        performance_scene_list.append(Performance_scene['scene'])
    return render(request, 'quickit/apm_offline.html', locals())

@check_login
def api_monitor(request):
    """
    api错误监控页面
    """
    username = request.session['username']
    add_log(username, '进入api错误监控页面', 'api_monitor')

    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    API_infos = models.APImoitor.objects.all().order_by('-id')
    projects = models.APImoitor.objects.values('project').distinct()
    errortypes = models.APImoitor.objects.values('errortype').distinct()
    projects_list = []
    for project in projects:
        projects_list.append(project['project'])
    errortype_list = []
    for errortype in errortypes:
        errortype_list.append(errortype['errortype'])
    return render(request, 'quickit/api_monitor.html', locals())

@check_login
def apm_detail(request,logname):
    """
    apm详情页面
    """
    username = request.session['username']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']

    add_log(username, '进入apm详情页面', 'apm_detail')
    nickname = request.session['nickname']
    apm_info = get_object_or_404(models.Performance, logname=logname)
    return render(request, 'quickit/apm_detail.html', locals())


@check_login
def offline_log(request):
    """
    埋点查询页面
    """
    username = request.session['username']
    add_log(username, '进入埋点查询页面', 'offline_log')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    anms = models.Server_applog.objects.values('anm').distinct()
    # anms_list = ['chalo786','shoora','vgame','vidmate','vmplayer','vdprivacy','transnow','utranit','kabuli']
    anms_list = []
    for anm in anms:
        anms_list.append(anm['anm'])
    return render(request, 'quickit/offline_log.html', locals())

def offline_log_search(request):
    """
    埋点查询接口
    """
    anm = request.POST.get("anm")
    filter = request.POST.get("filter")
    username = request.session['username']
    add_log(username, '调用埋点查询接口', 'offline_log_search')
    keyword = str(request.POST.get("keyword")).strip()
    if anm == 'All':
        if keyword == "":
            data = models.Server_applog.objects.all().order_by('-logtime')[:100]
        elif keyword != '':
            if filter == 'ACTION':
                data = models.Server_applog.objects.filter(action__contains =  keyword).order_by('-logtime')[:100]
            elif filter == 'DID':
                data = models.Server_applog.objects.filter(did__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'SUBANM':
                data = models.Server_applog.objects.filter(subanm__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'BRD':
                data = models.Server_applog.objects.filter(brd__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'VERSION':
                data = models.Server_applog.objects.filter(ver__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'PROJECT':
                data = models.Server_applog.objects.filter(project__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'TYPE':
                data = models.Server_applog.objects.filter(type__contains= keyword).order_by('-logtime')[:100]
    elif anm != 'All':
        if keyword == "":
            data = models.Server_applog.objects.filter(anm=anm).order_by('-logtime')[:100]
        elif keyword != '':
            if filter == 'ACTION':
                data = models.Server_applog.objects.filter(anm=anm,action__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'DID':
                data = models.Server_applog.objects.filter(anm=anm,did__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'SUBANM':
                data = models.Server_applog.objects.filter(subanm__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'BRD':
                data = models.Server_applog.objects.filter(anm=anm,brd__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'VERSION':
                data = models.Server_applog.objects.filter(anm=anm,ver__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'PROJECT':
                data = models.Server_applog.objects.filter(anm=anm,project__contains= keyword).order_by('-logtime')[:100]
            elif filter == 'TYPE':
                data = models.Server_applog.objects.filter(anm=anm,type__contains= keyword).order_by('-logtime')[:100]
    logdata_list = []
    for log in data:
        log_data = []
        log_data.append(log.anm)
        log_data.append(log.subanm)
        log_data.append(log.action)
        log_data.append(log.did)
        log_data.append(log.brd)
        log_data.append(log.ver)
        log_data.append(str(log.logcontent).replace('\"',''))
        log_data.append(str(log.logtime))
        logdata_list.append(log_data)
    result = {'code': 200, 'msg': 'success','logdata':logdata_list}

    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def applog(request):
    """
    app日志查询页面
    """
    username = request.session['username']
    add_log(username, '进入app日志查询页面', 'applog')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    AppLogDatas = models.Applog.objects.all().order_by('-id')[:1000]
    package_names = models.Applog.objects.values('pkgname').distinct()
    app_list = []
    for package_name in package_names:
        app_list.append(package_name['pkgname'])
    return render(request, 'quickit/applog.html', locals())

@check_login
def applog_detail(request,logname):
    """
    app日志详情页面
    """
    username = request.session['username']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']

    add_log(username, '进入app日志详情页面', 'applog_detail')
    nickname = request.session['nickname']
    applog_info = get_object_or_404(models.Applog, logname=logname)
    return render(request, 'quickit/applog_detail.html', locals())

@check_login
def applog_search_api(request):
    """
    app日志查询接口
    """
    project = str(request.POST.get("project")).strip()
    filter = str(request.POST.get("filter")).strip()
    keyword = str(request.POST.get("keyword")).strip()
    username = str(request.session['username'])
    sdate = str(request.POST.get("sdate")).strip()
    edate = str(request.POST.get("edate")).strip()
    add_log(username, 'app日志查询接口', 'applog_search_api')
    start_year = int(sdate.split("-")[0])
    start_month = int(sdate.split("-")[1])
    start_day = int(sdate.split("-")[2])
    start_h = 0
    start_m = 0
    start_s = 0

    end_year = int(edate.split("-")[0])
    end_month = int(edate.split("-")[1])
    end_day = int(edate.split("-")[2])
    end_h = 23
    end_m = 59
    end_s = 59
    if project == 'All' or project=='':
        if keyword == "":
            data = models.Applog.objects.filter(ctime__gte=datetime.datetime(start_year,start_month,start_day,start_h,start_m,start_s),
                                                    ctime__lte=datetime.datetime(end_year,end_month,end_day,end_h,end_m,end_s)).order_by('-ctime')[:1000]
        elif keyword != '':
            if filter == 'DID':
                data = models.Applog.objects.filter(did__contains= keyword,
                                                    ctime__gte=datetime.datetime(start_year,start_month,start_day,start_h,start_m,start_s),
                                                    ctime__lte=datetime.datetime(end_year,end_month,end_day,end_h,end_m,end_s)).order_by('-ctime')[:1000]
            elif filter == 'VERSION':
                data = models.Applog.objects.filter(version__contains= keyword,ctime__gte=datetime.datetime(start_year,start_month,start_day,start_h,start_m,start_s),
                                                    ctime__lte=datetime.datetime(end_year,end_month,end_day,end_h,end_m,end_s)).order_by('-ctime')[:1000]
            elif filter == 'REMARK':
                data = models.Applog.objects.filter(remark__contains= keyword,ctime__gte=datetime.datetime(start_year,start_month,start_day,start_h,start_m,start_s),
                                                    ctime__lte=datetime.datetime(end_year,end_month,end_day,end_h,end_m,end_s)).order_by('-ctime')[:1000]
    elif project != 'All':
        if keyword == "":
            data = models.Applog.objects.filter(pkgname=project,ctime__gte=datetime.datetime(start_year,start_month,start_day,start_h,start_m,start_s),
                                                    ctime__lte=datetime.datetime(end_year,end_month,end_day,end_h,end_m,end_s)).order_by('-ctime')[:1000]
        elif keyword != '':
            if filter == 'DID':
                data = models.Applog.objects.filter(pkgname=project,did__contains= keyword,ctime__gte=datetime.datetime(start_year,start_month,start_day,start_h,start_m,start_s),
                                                    ctime__lte=datetime.datetime(end_year,end_month,end_day,end_h,end_m,end_s)).order_by('-ctime')[:1000]
            elif filter == 'VERSION':
                data = models.Applog.objects.filter(pkgname=project,version__contains= keyword,ctime__gte=datetime.datetime(start_year,start_month,start_day,start_h,start_m,start_s),
                                                    ctime__lte=datetime.datetime(end_year,end_month,end_day,end_h,end_m,end_s)).order_by('-ctime')[:1000]
            elif filter == 'REMARK':
                data = models.Applog.objects.filter(pkgname=project,remark__contains= keyword,ctime__gte=datetime.datetime(start_year,start_month,start_day,start_h,start_m,start_s),
                                                    ctime__lte=datetime.datetime(end_year,end_month,end_day,end_h,end_m,end_s)).order_by('-ctime')[:1000]
    logdata_list = []
    for log in data:
        log_data = []
        log_data.append(log.id)
        log_data.append(log.pkgname)
        log_data.append(log.version)
        log_data.append(log.logname)
        log_data.append(log.did)
        log_data.append(log.remark)
        log_data.append(str(log.ctime))
        logdata_list.append(log_data)
    result = {'code': 200, 'msg': 'success','logdata':logdata_list}

    return HttpResponse(json.dumps(result), content_type="application/json")


@check_login
def ci_server(request):
    username = request.session['username']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    add_log(username, '进入ci_server页面', 'ci_server')
    nickname = request.session['nickname']
    return render(request, 'quickit/ci_server.html', locals())


@check_login
def delete_data(request):
    username = request.session['username']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    if admin_type == "1":
        apk_name = request.GET.get("apk_name")
        add_log(username, '删除apkname:%s'%apk_name, 'delete_data')
        models.Apk.objects.filter(apk_name=apk_name).delete()
        models.Size.objects.filter(apk_name=apk_name).delete()
        result = {'code': 200, 'msg': 'delete suc'}
    else:
        result = {'code': 202, 'msg': 'delete fail'}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def get_size(request):
    apk_name = request.GET.get("apk_name")
    username = request.session['username']
    add_log(username, '获取apkname:%s的size' % apk_name, 'get_size')
    sql_data = models.Size.objects.filter(apk_name = apk_name)
    size = models.Apk.objects.filter(apk_name = apk_name).values("size").first()['size']
    data = {}
    for var in sql_data:
        data["apk_name"] = var.apk_name
        data["size"] = size
        data['dex'] = var.dex
        data['so'] = var.so
        data['xml'] = var.xml
        data['arsc'] = var.arsc
        data['jar'] = var.jar
        data['SF'] = var.SF
        data['MF'] = var.MF
        data['kotlin_metadata'] = var.kotlin_metadata
        data['jpg'] = var.jpg
        data['gz'] = var.gz
        data['png'] = var.png
        data['gif'] = var.gif
        data['webp'] = var.webp
        data['mp4'] = var.mp4
        data['properties'] = var.properties
        data['kotlin_module'] = var.kotlin_module
        data['kotlin_builtins'] = var.kotlin_builtins
    rep = json.dumps(data)
    return HttpResponse(rep)

@check_login
def change_password_page(request):
    username = request.session['username']
    add_log(username, '修改密码页面' , 'change_password_page')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    return render(request, 'quickit/change_password.html', locals())

@check_login
def change_password_api(request):
    new_pwd = request.POST.get("new_pwd")
    old_pwd = request.POST.get("old_pwd")
    username = request.session['username']
    get_old_pwd = models.User.objects.filter(username=username,password=old_pwd)
    if get_old_pwd:
        models.User.objects.filter(username=username).update(password=new_pwd)
        add_log(username, '修改密码成功', 'change_password_api')
        result = {'code': 200, 'msg': 'change success'}
    else:
        result = {'code': 202, 'msg': 'old password wrong!'}
        add_log(username, '修改密码失败', 'change_password_api')
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def TItest(request):
    username = request.session['username']
    add_log(username, 'TItest', 'TItest')
    version = request.POST.get("version")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    try:
        if version =="3.14":
            result = {'code': 200, 'msg': 'success', 'data':
                [[
                    {
            "date":"2020-01-01",
            "version":"3.14",
            "apmdata":3
        },
                    {
            "date":"2020-01-02",
            "version":"3.14",
            "apmdata":4
        },
                    {
            "date": "2020-01-03",
            "version": "3.14",
            "apmdata": 5
        },
                    {
                        "date": "2020-01-03",
                        "version": "3.14",
                        "apmdata": 10
                    },
                    {
                        "date": "2020-01-03",
                        "version": "3.14",
                        "apmdata": 3
                    },
                    {
            "date": "2020-01-03",
            "version": "3.14",
            "apmdata": 11
        },
                    {
                        "date": "2020-01-03",
                        "version": "3.14",
                        "apmdata": 7
                    }
                ]]}
        else:
            result = {'code': 200, 'msg': 'success', 'data':
                [[
                    {
                        "date": "2020-01-01",
                        "version": "3.15",
                        "apmdata": 6
                    },
                    {
                        "date": "2020-01-02",
                        "version": "3.15",
                        "apmdata": 7
                    },
                    {
                        "date": "2020-01-03",
                        "version": "3.15",
                        "apmdata": 8
                    },
                    {
                        "date": "2020-01-03",
                        "version": "3.15",
                        "apmdata": 20
                    },
                    {
                        "date": "2020-01-03",
                        "version": "3.15",
                        "apmdata": 3
                    },
                    {
                        "date": "2020-01-03",
                        "version": "3.15",
                        "apmdata": 10
                    },
                    {
                        "date": "2020-01-03",
                        "version": "3.15",
                        "apmdata": 8
                    }
                ]]}

    except:
        result = {'code': 202, 'msg': 'Error'}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def apm_api(request):
    username = request.session['username']
    pkgname = request.POST.get("pkgname")
    scene = request.POST.get("scene")
    compare_project = request.POST.get("compare_project")
    add_log(username, '查看%s的apm'%pkgname, 'apm_api')
    TimeCost_datas = models.StartUpTime.objects.raw('Select * from QuickTI.testsite_startuptime where status=\'Online\' and pkgname=\''+str(pkgname).strip()+'\' and scene=\''+str(scene).strip()+'\'')
    Compare_TimeCost_data  = models.StartUpTime.objects.filter(pkgname=str(compare_project).strip(), status='Competitor',scene=scene).values("timecost").first()['timecost']

    Time_data = []
    Compare_TimeCost_data_list = []
    Version = []
    if pkgname:
        for TimeCost_data in TimeCost_datas:
            Time_data.append(TimeCost_data.timecost)
            Version.append(TimeCost_data.version)
            Compare_TimeCost_data_list.append(Compare_TimeCost_data)
        result = {'code': 200, 'Time_data': Time_data,'Version':Version,'Compare_data':Compare_TimeCost_data_list}
    else:
        result = {'code': 202, 'mag':'no pkgname data'}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def apm_detail_api(request):
    logname = request.POST.get("logname")
    Compare_project = request.POST.get("Compare_project")
    username = request.session['username']
    add_log(username, '查看logname=%s'%logname, 'apm_detail_api')
    logdir = '/home1/www/tomcat/apache-tomcat-9.0.27/webapps/examples/nemo/TI/apmlog/'
    logflag =os.path.exists(logdir+logname)
    project  = models.Performance.objects.filter(logname=str(logname).strip()).values("pkgname").first()['pkgname']

    project_scene  = models.Performance.objects.filter(logname=str(logname).strip()).values("scene").first()['scene']
    Competitor_project = models.Performance.objects.filter(scene=str(project_scene),status='Competitor')

    Competitor_project_list=[]
    for Competitor_project_data in Competitor_project:
        Competitor_project_list.append(Competitor_project_data.pkgname)
    content=[]
    competitor_content = []
    if Compare_project != 'NA':
        Competitor_logname = \
        models.Performance.objects.filter(pkgname=str(Compare_project).strip(), scene=str(project_scene),
                                          status='Competitor').values("logname").first()['logname']
        if logname and logflag == True and Competitor_logname:
            apmfile = open(logdir + str(logname), "r")
            for line in apmfile.readlines():
                content_time = line.strip().split(":")[0]
                content_apm = json.loads(line.strip().split(":")[1])
                jsondata = {"time": content_time, "apmdata": content_apm}
                content.append(jsondata)
            apmfile.close()
            competitor_apmfile = open(logdir + str(Competitor_logname), "r")
            for line in competitor_apmfile.readlines():
                content_time = line.strip().split(":")[0]
                content_apm = json.loads(line.strip().split(":")[1])
                jsondata = {"time": content_time, "apmdata": content_apm}
                competitor_content.append(jsondata)
            competitor_apmfile.close()
            result = {'code': 200, 'msg': 'success', 'project':project,'data': content,
                      'Competitor_project_list': Competitor_project_list, 'Competitor_data': competitor_content}
        else:
            result = {'code': 202, 'msg': 'no logname', 'Competitor_project_list': Competitor_project_list}
    else:
        if logname and logflag == True:
            apmfile = open(logdir + str(logname), "r")
            for line in apmfile.readlines():
                content_time = line.strip().split(":")[0]
                content_apm = json.loads(line.strip().split(":")[1])
                jsondata = {"time": content_time, "apmdata": content_apm}
                content.append(jsondata)
            apmfile.close()
            result = {'code': 200, 'msg': 'success','project':project, 'data': content,
                      'Competitor_project_list': Competitor_project_list}
        else:
            result = {'code': 202, 'msg': 'no logname', 'Competitor_project_list': Competitor_project_list}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def get_timecost_info(request):
    '''
    创建timecost数据信息接口
    '''
    if request.method=="POST":
        id  = request.POST.get("id")
    else:
        id  = request.GET.get("id")

    if id:
        project = models.StartUpTime.objects.filter(id=id).values("pkgname").first()['pkgname']
        timecost = models.StartUpTime.objects.filter(id=id).values("timecost").first()['timecost']
        status = models.StartUpTime.objects.filter(id=id).values("status").first()['status']
        scene = models.StartUpTime.objects.filter(id=id).values("scene").first()['scene']
        time_detail = models.StartUpTime.objects.filter(id=id).values("time_detail").first()['time_detail']


        timecost_info = {
            "project":project,
            "timecost":timecost,
            "status": status,
            "scene":scene
        }
        result = {'status': 1, 'data': timecost_info,'time_detail':time_detail}
    else:
        result = {'status': 0, 'msg': 'request data empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")

def insert_timecost(request):
    '''
    创建timecost数据接口
    '''
    if request.method=="POST":
        project = request.POST.get("project")
        version = request.POST.get("version")
        scene = request.POST.get('scene')
        timecost = request.POST.get("timecost")
        time_detail = request.POST.get("time_detail")
    else:
        project = request.GET.get("project")
        version = request.GET.get("version")
        scene = request.GET.get('scene')
        timecost = request.GET.get("timecost")
        time_detail = request.GET.get("time_detail")

    status = 'Offline'
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if project and version and scene and timecost:
        insert_timecost = models.StartUpTime(pkgname=project, version=version, scene=scene, timecost=timecost,
                                         status=status, ctime=ctime,time_detail=time_detail)
        insert_timecost.save()
        result = {'status': 1, 'msg': 'creat data success'}
    else:
        result = {'status': 0, 'msg': 'request data empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def update_timecost(request):
    '''
    更新timecost数据接口
    '''
    id = request.POST.get("id")
    project = request.POST.get("project")
    status = request.POST.get("status")
    timevalue = request.POST.get("timevalue")
    scene = request.POST.get("scene")
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if id and project and status and timevalue:
        models.StartUpTime.objects.filter(id=id).update(pkgname=project, status=status, timecost=timevalue, ctime=ctime,scene=scene)

        result = {'status': 1, 'msg': 'update task success'}

    else:
        result = {'status': 0, 'msg': 'request data empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def api_monitor_api(request):
    username = request.session['username']
    add_log(username, '调用api_monitor_api', 'api_monitor_api')

    project = request.GET.get("project")
    sdate = request.GET.get("sdate")
    edate = request.GET.get("edate")
    projectdata = models.APImoitor.objects.values('project').distinct()#获取所有项目
    alldate_list = commonFunc.getDatesByTimes(sdate,edate) #获取所有日期
    project_list = []
    errornum_list = []#计算每条数据的errornum
    ctime_list = []
    realerrornum_list=[]#合并datetime相同的数据
    apilist = []
    allapidata=[]
    new_errornum_list = []  # 计算每条数据的errornum
    for project_name in projectdata:
        project_list.append(project_name['project'])

    if project=='All':
        result = {'code': 200, 'project': project_list}
    else:
        # *****获取errornums统计*******
        i=0
        j=0
        while i < len(alldate_list):
            errornum_count=0
            api_datas = models.APImoitor.objects.raw(
                'SELECT * FROM QuickTI.testsite_apimoitor where project=\'' + str(project) + '\'' +
                ' and datetime= \'' + str(alldate_list[i])+ '\'')
            for api_data in api_datas:
                errornum_list.append(api_data.errortimes)
                ctime_list.append(api_data.ctime)
            while j < len(errornum_list):
                errornum_count = errornum_list[j] + errornum_count
                j = j + 1
            realerrornum_list.append(errornum_count)
            i = i+1
        jsondata =[{'project':project,'ctime': alldate_list, 'errornum': realerrornum_list}]

        # *****获取api统计*******
        api_datas = models.APImoitor.objects.filter(project=project)
        for api_data in api_datas:
            apilist.append(api_data.api)
        apilist = list(set(apilist))
        k=0
        while k<len(apilist):
            errornum_count=0
            h=0
            new_errornum_list=[]
            api_datas = models.APImoitor.objects.raw(
                'SELECT * FROM QuickTI.testsite_apimoitor where project=\'' + str(project) + '\'' +
                ' and api= \'' + str(apilist[k]) + '\'' )
            for api_data in api_datas:
                new_errornum_list.append(api_data.errortimes)
            while h < len(new_errornum_list):
                errornum_count = new_errornum_list[h] + errornum_count
                h = h + 1

            api_jsondata = {'api': str(apilist[k]).replace('\n','').strip(),  'errornum': errornum_count}
            allapidata.append(api_jsondata)
            k = k + 1
        result = {'code': 200, 'project': project_list, 'data': jsondata,'apidata':allapidata}

    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def applog_api(request):
    '''
    app日志操作接口
    '''
    logname = request.GET.get("logname")
    username = request.session['username']
    add_log(username, '操作app日志：%s'%logname, 'applog_api')
    log_detail_name = request.GET.get("log_detail_name")
    logdir = '/home1/www/tomcat/apache-tomcat-9.0.27/webapps/examples/nemo/TI/applog/'
    logname_dir = logname.replace('.zip', '')
    current_dir = os.getcwd()
    allfilename = commonFunc.get_file_name_list(logdir+logname_dir)
    logflag =os.path.exists(logdir+logname_dir)
    content=''

    if logflag==True:
        if log_detail_name:
            applogfile = open(logdir + logname_dir + '/' + log_detail_name, "r")
            content = applogfile.read()
            applogfile.close()
            result = {'code': 200, 'msg': 'success', 'data': content, 'filelist': allfilename}
        else:
            applogfile = open(logdir +logname_dir + '/' + allfilename[0], "r")
            content = applogfile.read()
            applogfile.close()
            result = {'code': 200, 'msg': 'success', 'data': content, 'filelist': allfilename}
    else:
        os.chdir(logdir)
        os.system('mkdir '+logname_dir)
        os.system('unzip ' + logname+' -d '+logname_dir)
        os.chdir(current_dir)
        allfilename = commonFunc.get_file_name_list(logdir + logname_dir)
        if log_detail_name:
            applogfile = open(logdir + logname_dir + '/' + log_detail_name, "r")
            content = applogfile.read()
            applogfile.close()
            result = {'code': 200, 'msg': 'success', 'data': content, 'filelist': allfilename}
        else:
            applogfile = open(logdir + logname_dir + '/' + allfilename[0], "r")
            content = applogfile.read()
            applogfile.close()
            result = {'code': 200, 'msg': 'success', 'data': content, 'filelist': allfilename}

    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def ci_server_api(request):
    '''
    各个服务运维接口
    '''
    username = request.session['username']
    add_log(username, 'ci_server_api', 'ci_server_api')

    action = request.GET.get("action")
    type = request.GET.get("type")
    ls = request.GET.get("ls")
    Sprocess = request.GET.get("Sprocess")
    filelink = request.GET.get("filelink")
    if action=='Upload File':
        if filelink:
            response = requests.get(
                'http://47.88.153.30:8880/ciserver/download?type=' + type + '&filelink=' + filelink,
                verify=False).text
            Data = json.loads(response)
            result = Data['result']
            result = {'code': 200, 'result': result}
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            response = requests.get('http://47.88.153.30:8880/ciserver/download?type=' + type + '&ls=' + ls,
                                    verify=False).text
            Data = json.loads(response)
            content = Data['content']
            result = {'code': 200, 'content': content}
    elif action=='Restart Service':
        if type=='Maven' or type=='Jenkins' or type=='Code' or type=='Jira':
            if Sprocess:
                response = requests.get('http://47.106.194.167:8880/ciserver/restart?type=' + type+'&Sprocess='+Sprocess, verify=False).text
                Data = json.loads(response)
                result = Data['result']
                result = {'code': 200, 'result': result}
                return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                response = requests.get('http://47.106.194.167:8880/ciserver/restart?type=' + type, verify=False).text
                Data = json.loads(response)
                result = Data['status']
                result = {'code': 200, 'result': 'waiting 5 mins...'}
                return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            if Sprocess:
                response = requests.get('http://47.88.153.30:8085/oldserver/restart?type=' + type+'&Sprocess='+Sprocess, verify=False).text
                Data = json.loads(response)
                result = Data['process']
                result = {'code': 200, 'result': result}
                return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                response = requests.get('http://47.88.153.30:8085/oldserver/restart?type=' + type, verify=False).text
                Data = json.loads(response)
                result = Data['status']
                result = {'code': 200, 'result': 'waiting 5 mins...'}
                return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'code': 200, 'result': 'no deal'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def getCPUInfo(request):
    '''
    获取系统cpu损耗
    '''
    a = psutil.cpu_times_percent()
    user_percentage = a.user
    system_percentage = a.system
    return HttpResponse('{"user": %s,"system":%s}' % (user_percentage, system_percentage))

def insert_api(request):
    '''
    api信息入库接口
    '''
    project = request.POST.get("project")
    env = request.POST.get("env")
    apiname = str(request.POST.get("apiname")).replace("/","_")
    request_content = request.POST.get("request_content")
    response_content = request.POST.get("response_content")
    url = request.POST.get("url")
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    taskname = apiname+"_"+env
    creater = 'TI'
    if env and project and apiname and request_content and response_content and url:
        try:
            insert_api = models.APIinfo(project=project, env=env, api=apiname+"_"+env, request_name=request_content,
                                        response_name=str(response_content).replace("\\",""),
                                        url=url, ctime=ctime)
            insert_task = models.APItask(project=project, env=env, taskname=taskname, timercheck='true',
                                         timevalue=5,
                                         timetype='Min', creater=creater, ctime=ctime, case=str(response_content).replace("\\",""))
            insert_api.save()
            insert_task.save()
            result = {'status': 1, 'msg': 'insert api success'}
        except:
            models.APIinfo.objects.filter(api=apiname+"_"+env).update(request_name=request_content,
                                                              response_name=response_content, ctime=ctime)
            result = {'status': 1, 'msg': 'update api success'}
    else:
        result = {'status': 0, 'msg':'request data empty!'}
    return HttpResponse(json.dumps(result), content_type="application/json")

def getapi(request):
    '''
    获取api接口
    '''
    env = request.POST.get("env")
    project = str(request.POST.get("project")).strip()
    task =request.POST.get("task")
    username = request.session['username']
    add_log(username, '获取api接口,project:%s,env:%s,task:%s'%(project,env,task), 'getapi')

    api_list = []
    if task:
        url = models.APIinfo.objects.filter(api=task).values("url").first()['url']
        request_content = models.APIinfo.objects.filter(api=task).values("request_name").first()['request_name']
        response_content = models.APIinfo.objects.filter(api=task).values("response_name").first()['response_name']
        result = {'status': 1, 'url': url,'request_content':request_content,'response_content':response_content}
    else:
        if env and project:
            url_lists = models.APIinfo.objects.filter(project=project, env=env).values("url")
            for url_list in url_lists:
                api_list.append(url_list['url'])
            result = {'status': 1, 'result': api_list}
        else:
            result = {'status': 0, 'msg': 'request data empty!'}
    return HttpResponse(json.dumps(result), content_type="application/json")

def getpost(request):
    '''
    获取请求和返回内容接口
    '''
    type = request.POST.get("type")
    url = str(request.POST.get("url")).strip()

    username = request.session['username']
    add_log(username, '获取请求和返回内容接口,type:%s'%type, 'getpost')

    if type == 'request':
        request_content = models.APIinfo.objects.filter(url=url).values("request_name").first()['request_name']
        '''
        request_dir = os.getcwd() + '/testsite/apidata/request.json'
        f = open(request_dir, encoding='utf-8')
        request_txt = f.read()'''
        result = {'status': 1, 'result': request_content}
    else:
        response_content = models.APIinfo.objects.filter(url=url).values("response_name").first()['response_name']
        '''response_dir = os.getcwd() + '/testsite/apidata/response.json'
        f = open(response_dir, encoding='utf-8')
        response_txt = f.read()'''
        result = {'status': 1, 'result': response_content}
    return HttpResponse(json.dumps(result), content_type="application/json")

def apipost(request):
    '''
    api请求接口
    '''
    payload = request.POST.get("payload")
    url = request.POST.get("url")
    post_type = request.POST.get("post_type")

    username = request.session['username']
    add_log(username, 'api请求接口,payload:%s,url:%s,post_type:%s'%(payload,url,post_type), 'apipost')

    if post_type == 'curl':
        response = commonFunc.execCmd(payload)
        result = {'status': 1, 'result': response}
    elif post_type == 'get':
        response = commonFunc.getTopost(payload)
        result = {'status': 1, 'result': response}
    else:
        if payload and url:
            response = commonFunc.GetResponse(payload, str(url).strip(), "All")
            result = {'status': 1, 'result': response}
        else:
            result = {'status': 0, 'result': 'request empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")

def insert_task(request):
    '''
    创建任务接口
    '''
    project = request.POST.get("project")
    env = request.POST.get("env")
    taskname = request.POST.get('taskname')
    timercheck = request.POST.get("timercheck")
    timevalue = int(request.POST.get("timevalue"))
    timetype = request.POST.get('timetype')
    creater = request.POST.get('creater')
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    #username = request.session['username']
    #add_log(username, '创建任务接口,project:%s,env:%s,taskname:%s'%(project,env,taskname), 'insert_task')

    if project and env and taskname and timercheck and timetype:
        try:
            taskname= str(taskname).replace('\\','_')
            insert_api = models.APIinfo(project=project, env=env, api=taskname, request_name='{}',
                                        response_name='{}',url="", ctime=ctime)
            insert_task = models.APItask(project=project, env=env, taskname=taskname, timercheck=timercheck,
                                         timevalue=timevalue, timetype=timetype, creater=creater, ctime=ctime)
            insert_api.save()
            insert_task.save()
            result = {'status': 1, 'msg': 'insert task success'}
        except:
            result = {'status': 0, 'msg': 'task existed'}
    else:
        result = {'status': 0, 'msg': 'request data empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")


def update_task(request):
    update_type = request.POST.get("update_type")
    status = request.POST.get("status")
    id = request.POST.get("id")
    case = request.POST.get("case")

    project = request.POST.get("project")
    env = request.POST.get("env")
    timercheck = request.POST.get("timercheck")
    timetype = request.POST.get("timetype")
    timevalue = request.POST.get("timevalue")

    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if update_type=='status':
        if status and id:

            models.APItask.objects.filter(id=id).update(status=status,ctime=ctime)
            result = {'status': 1, 'msg': 'update task success'}
        else:
            result = {'status': 0, 'msg': 'request data empty'}
    else:
        if case:
            models.APItask.objects.filter(id=id).update(case=case, ctime=ctime)
            result = {'status': 1, 'msg': 'update case success'}
        else:
            models.APItask.objects.filter(id=id).update(project=project,env=env,timercheck=timercheck,timetype=timetype,timevalue=timevalue, ctime=ctime)
            result = {'status': 1, 'msg': 'update task success'}
    return HttpResponse(json.dumps(result), content_type="application/json")

def get_task(request):
    if request.method=="POST":
        id  = request.POST.get("id")
        timercheck = request.POST.get("timercheck")
    else:
        id  = request.GET.get("id")
        timercheck = request.GET.get("timercheck")

    if timercheck:
        taskinfo = models.APItask.objects.filter(timercheck=timercheck)
        taskdata_list = []

        for tasks in taskinfo:
            task_data = []
            task_data.append(tasks.id)
            task_data.append(tasks.env)
            task_data.append(tasks.project)
            task_data.append(tasks.taskname)
            taskdata_list.append(task_data)
        result = {'status': 1, 'msg': 'get task success','data':taskdata_list}

    elif id:
        project = models.APItask.objects.filter(id=id).values("project").first()['project']
        env = models.APItask.objects.filter(id=id).values("env").first()['env']
        task = models.APItask.objects.filter(id=id).values("taskname").first()['taskname']
        timer = models.APItask.objects.filter(id=id).values("timercheck").first()['timercheck']
        timetype = models.APItask.objects.filter(id=id).values("timetype").first()['timetype']
        timevalue = models.APItask.objects.filter(id=id).values("timevalue").first()['timevalue']
        task_result = {
            "project":project,
            "env":env,
            "task":task,
            "timer":timer,
            "timetype":timetype,
            "timevalue":timevalue
        }
        result = {'status': 1, 'data': task_result}
    else:
        result = {'status': 0, 'msg': 'request data empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")

def run_task(request):
    '''
    执行任务接口
    '''
    if request.method == "POST":
        id = request.POST.get("id")
        project = request.POST.get("project")
        task = request.POST.get("task")
        env = request.POST.get("env")
    else:
        id = request.GET.get("id")
        project = request.GET.get("project")
        task = request.GET.get("task")
        env = request.GET.get("env")

    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    status = 'None'
    result_list=[]
    error_list=[]
    passcount = 0
    errorcount = 0

    if project and task:
        url = models.APIinfo.objects.filter(api=task, project=project).values("url").first()['url']
        request_content = models.APIinfo.objects.filter(api=task, project=project).values("request_name").first()[
            'request_name']
        response_content = models.APIinfo.objects.filter(api=task, project=project).values("response_name").first()[
            'response_name']
        cases = models.APItask.objects.filter(id=id).values("case").first()['case']
        cases_json = json.loads(cases)
        check_type_list = list(cases_json.keys())
        i = 0
        j = 0
        h = 0
        code = commonFunc.GetResponse(request_content, url, "code")
        stopjob = commonFunc.Equal('code', code, "200", error_list)

        if stopjob=='false':
            try:
                base_response = commonFunc.GetResponse(request_content, url, "All")
                response = json.loads(commonFunc.GetResponse(request_content, url, "All"))
                while len(check_type_list) > i:
                    check_name_list = list(cases_json[check_type_list[i]].keys())
                    check_value_list = list(cases_json[check_type_list[i]].values())
                    try:
                        if check_type_list[i] == 'Equal':
                            while len(check_name_list) > j:
                                commonFunc.Equal(check_name_list[j], response[check_name_list[j]], check_value_list[j],
                                                 error_list)
                                j = j + 1
                        elif check_type_list[i] == 'Len':
                            while len(check_name_list) > h:
                                commonFunc.LengthCheck(check_name_list[h], len(response[check_name_list[h]]),
                                                       error_list)
                                h = h + 1
                    except:
                        errorinfo = {
                            "name": "Case error",
                            "info": str(traceback.format_exc())
                        }
                        error_list.append(errorinfo)
                    i = i + 1
                if len(error_list) > 0:
                    status = 'Error'
                    errorcount = errorcount + 1
                else:
                    status = 'Success'
                    passcount = passcount + 1
            except:
                errorinfo = {
                    "name": "Case error",
                    "info": str(traceback.format_exc())
                }
                error_list.append(errorinfo)
                status = 'Error'
                errorcount = errorcount + 1

        else:
            base_response='null'
            status = 'Error'
            passcount=0
            errorcount=1

        result = {"time": ctime,
                  "url": url,
                  "request": json.loads(request_content),
                  "response": base_response,
                  "error": error_list
                  }

        result_list.append(result)
        insert_result = models.Taskresult(project=project, env=env, taskname=task, status=status,
                                          result=result_list,
                                          ctime=ctime, errorcount=errorcount, passcount=passcount)

        Data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "API错误告警",
                "text": "\n > #### Project: " + project  \
                        + "\n > #### Env: " + env \
                        + "\n > #### Url: " + str(url) \
                        + "\n > #### Request: \n" + str(request_content).replace(" ","").replace("\n","").replace("\t","") \
                        + "\n > #### Response: \n" + str(base_response) \
                        + "\n > #### Error: \n" + str(error_list)
                        + "\n > #### [Test Report](http://ti.flatincbr.com:8887/report/"+task+")"

            },
            "at": {
                "atMobiles": ["13524352709"],
                "isAtAll": False
            }
        }
        if status == 'Error':
            commonFunc.dingding_robot(Data)
            pass
        insert_result.save()
        models.APItask.objects.filter(id=id).update(status=status, ctime=ctime)
        result = {'code': 200, 'msg': 'run task success', 'result': base_response, 'status': status, 'passcount': passcount,
                  'errorcount': errorcount}
    else:
        result = {'code': 202, 'msg': 'request data empty'}

    return HttpResponse(json.dumps(result), content_type="application/json")


def update_case(request):
    id = request.POST.get("id")
    url = request.POST.get("url")
    api = request.POST.get("api")
    request_content = request.POST.get("request_content")
    case = request.POST.get("case")
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if id and api and request_content and case:
        if '&' in request_content:
            request_content= commonFunc.getTojson(request_content)
        models.APIinfo.objects.filter(api=api).update(url=url,request_name=request_content, response_name=case,
                                                      ctime=ctime)
        models.APItask.objects.filter(id=id).update(case=case, ctime=ctime)
        result = {'status': 1, 'msg': 'update case success'}
    else:
        result = {'status': 0, 'msg': 'request data empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")

# 添加定时任务,remark唯一
def task_add(request):

    task_name = request.POST.get("task_name")
    timer = request.POST.get("timer")
    remark = request.POST.get("remark")
    username = request.session['username']
    add_log(username, '添加定时任务,task_name:%s,timer:%s,remark:%s' % (task_name, timer, remark), 'task_add')

    # 创建linux系统当前用户的crontab，当然也可以创建其他用户的，但得有足够权限,如:user='root'
    cron_manager = CronTab(user=True)

    # 检查该任务是否已存在
    jobs = cron_manager.find_comment(remark)
    if len(jobs) == 0:
    # 创建任务 指明运行python脚本的命令(crontab的默认执行路径为：当前用户的根路径, 因此需要指定绝对路径)
        job = cron_manager.new(
            command="python3 testsite/crontab_task.py %s" % task_name)

        job.setall(timer)
        job.set_comment(remark)
        # 将crontab写入linux系统配置文件
        cron_manager.write()

        result={'status': 1, 'result': "task add succ"}
    else:

        result = {'status': 0, 'result': "task existed"}

    return HttpResponse(json.dumps(result), content_type="application/json")

# 删除定时任务
def task_del(request):
    # 创建linux系统当前用户的crontab
    cron_manager = CronTab(user=True)

    remark = request.POST.get("remark")

    jobs = cron_manager.find_comment(remark)

    username = request.session['username']
    add_log(username, '删除定时任务,cron_manager:%s,remark:%s,jobs:%s' % (cron_manager, remark, jobs), 'task_del')

    if len(jobs) == 0:
        result = {'status': 0, 'result': "task not existed"}
    else:
        cron_manager.remove_all(comment=remark)
        cron_manager.write()
        result={'status': 1, 'result': "task del succ"}

    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
# 查询配置
def query_config_api(request):
    env = request.POST.get("env")
    anm = request.POST.get("anm")
    appid = request.POST.get("appid")
    appver = request.POST.get("appver")
    appverc = request.POST.get("appverc")
    bucket = request.POST.get("bucket")
    language = request.POST.get("language")
    country = request.POST.get("country")
    pkg = request.POST.get("pkg")
    pf = request.POST.get("pf")
    type = request.POST.get("type")
    dev_channel = request.POST.get("dev_channel")
    brd = request.POST.get('brd')
    loc = request.POST.get('loc')
    install_time = request.POST.get('install_time')

    username = request.session['username']
    add_log(username, '查询%s配置' % type, 'query_config_api')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    if bucket != '':
        if bucket[0]== 'S' :
            bucket = int(bucket[1])-1
        elif bucket[0]== 'L' :
            bucket = int(bucket[1])*10 + 5
    if type == 'appconfig':
        if anm == "vidmate":
            if env == "Test":
                url = "http://api.test.vidmate.net/api/cmsflow/config/config_v2"
            else:
                url = "http://api.v-mate.mobi/api/cmsflow/config/config_v2"

            data = 'anm=vidmate&appid=%s&' \
                   'appver=%s&bucket=%s&sign=n_e_m_o&' \
                   'debug=nemo&country=%s&lanuage=%s&pkg=%s&brand=%s' % (appid, appver, bucket, country, language, pkg,brd)
            r = json.loads(requests.post(url, headers=headers, data=data).text.replace(r"\\", ""))
            host = url.split("/api/")[0][7:]
            curl = "curl -H 'Host: {host}' -H 'User-Agent: python-requests/2.22.0' -H 'Accept: */*' --data '{data}'--compressed '{url}'".format(host=host,data=data,url=url)
        else:
            if env == "Test":
                url = "http://47.74.180.115:8009/api/appconfig/config/get"
            else:
                url = "http://api.flatfishsafe.com/api/appconfig/config/get"
            data = 'abslot=&aid=21585c979e0d0461&anm=%s' \
                   '&brd=%s&bucket=%s&cha=%s&cou=%s&mod=V1934A&net=wifi&os=28&pkg=%s&sdmounted=1' \
                   '&section_utimes=&sign=n_e_m_o&slan=%s' \
                   '&ver=%s&verc=%s&debug=nemo&pf=%s' % (
                   anm,brd, bucket, appid, country, pkg, language, appver, appverc, pf)
            r = json.loads(requests.post(url, headers=headers, data=data, verify=False).json()["data"].replace(r"\\", ""))
            host = url.split("/api/")[0][7:]
            curl = "curl -H 'Host: {host}' -H 'User-Agent: python-requests/2.22.0' -H 'Accept: */*' --data '{data}'--compressed '{url}'".format(
                host=host, data=data, url=url)


    elif type =='mediation':
        if appid == '':
            appid = 'no_input_cha'
        if install_time !='':
            hours = int(install_time)
            install_time = int(round(time.time() * 1000)) - hours * 60 * 60 * 1000
        data = 'abslot=&aid=21585c979e0d0461&anm=%s' \
               '&brd=%s&bucket=%s&cha=%s&cou=%s&mod=V1934A&net=wifi&os=28&pkg=%s&sdmounted=1' \
               '&section_utimes=&sign=n_e_m_o&location=%s' \
               '&ver=%s&verc=%s&debug=nemo&pf=%s&dev_channel=%s&dev_first_install_time=%s' % (
                   anm,brd, bucket, appid, country, pkg, loc, appver, appverc, pf,dev_channel,install_time )
        if env == "Test":
            url = "http://api.test.v-mate.mobi/api/adserver/mediation/get/"
        else:
            url = "http://api.apk.v-mate.mobi/api/adserver/mediation/get/"
        r = requests.post(url, headers=headers, data=data, verify=False).json()
        host = url.split("/api/")[0][7:]
        curl = "curl -H 'Host: {host}' -H 'User-Agent: python-requests/2.22.0' -H 'Accept: */*' --data '{data}'--compressed '{url}'".format(
            host=host, data=data, url=url)
    result = {'code': 200, 'result': r,'curl':curl}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def query_config(request):
    """
    查询配置
    """
    username = request.session['username']
    add_log(username, '进入查询配置页面', 'query_config')
    nickname = request.session['nickname']
    anms = models.Server_applog.objects.values('anm').distinct()
    # anms_list = ['chalo786','shoora','vgame','vidmate','vmplayer','vdprivacy','transnow','utranit','kabuli']
    anms_list = []
    for anm in anms:
        anms_list.append(anm['anm'])
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    return render(request, 'quickit/query_config.html', locals())

def galo_test(request):
    """
    galo金币修改
    """
    if request.method == "GET":
        action = request.GET.get("action")
        user_id = request.GET.get("user_id")
        score = request.GET.get("score")
        flag = request.GET.get("flag")
    else:
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")
        score = request.POST.get("score")
        flag = request.POST.get("flag")
    db = MySQLdb.connect("161.117.2.188", "tester2020", "Flatincbr.com", "nemo_activity", charset='utf8')
    cursor = db.cursor()
    if action=='search':
        sql = """SELECT activity_id,code,invite_code,phone,score,paytm,cash_out FROM nemo_activity.user_activity where  user_id = \'"""+user_id+"""\'"""
        cursor.execute(sql)
        results = cursor.fetchall()
        sql_data={}
        result_list = []
        for row in results:
            sql_data={
               "activity_id": row[0],
                "code":row[1],
                "invite_code":row[2],
                "phone":row[3],
                "score":row[4],
                "paytm":row[5],
                "cash_out":row[6]
            }
            result_list.append(sql_data)
        result = {'status': 1, 'msg': 'success','data':result_list}
    elif action=='update':
        sql = "update nemo_activity.user_activity set score =\""+ score+ "\"where user_id = \'"+user_id+"\'"
        try:
            cursor.execute(sql)
            db.commit()
            result = {'status': 1, 'msg': 'success'}
        except:
            db.rollback()
            result = {'status': 1, 'msg': 'fail','error':str(traceback.format_exc())}
    elif action == 'redis':
        refresh_redis_offline = requests.get("http://api.test.v-mate.mobi/api/nemo_activity/user/clean?actId=88&anm=vgame&uid="+user_id, verify=False)
        refresh_redis_online = requests.get("http://api.v-mate.mobi/api/nemo_activity/user/clean?actId=88&anm=vgame&uid="+user_id, verify=False)

        result = {'status': 1, 'offline': refresh_redis_offline.text,'online': refresh_redis_online.text}
    elif action=='review':
        db = MySQLdb.connect("161.117.2.188", "nemo_starhalo_be", "S4MZ6iUqkvx5O1ahfZ7C", "fleets_order", charset='utf8',port=3307)
        cursor = db.cursor()
        if flag=='true':
            update_sql = "update fleets_order.withdraw_record set wd_status =400 where uid =\'"+user_id +"\' order by id desc limit 1"
        else:
            update_sql = "update fleets_order.withdraw_record set wd_status =100 where uid =\'"+user_id +"\' order by id desc limit 1"
        try:
            cursor.execute(update_sql)
            db.commit()
            search_sql = "SELECT wd_status FROM fleets_order.withdraw_record where uid = \'"+user_id+"\' order by id desc limit 1"
            cursor.execute(search_sql)
            results = cursor.fetchall()
            wd_status = ''
            for row in results:
                wd_status = row[0]
            result = {'status': 1, 'msg': 'success','wd_status':wd_status}
        except:
            db.rollback()
            result = {'status': 1, 'msg': 'fail','error':str(traceback.format_exc())}
    else:
        result = {'status': 0, 'msg': 'action empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")

def make_phone(request):
    """
    制造测试手机号码
    """
    if request.method == "GET":
        anm = request.GET.get("anm")
        prefix= request.GET.get("prefix")

    else:
        anm = request.POST.get("anm")
        prefix = request.POST.get("prefix")

    if anm:
        maker = requests.get("http://47.74.180.115:6001/test/gen_test_phone?sign=n_e_m_o&anm="+anm+"&size=2&prefix=%2B"+prefix)
        result_list=json.loads(maker.text)['data']
        result = {'status': 1, 'msg': 'success','data':result_list}

    else:
        result = {'status': 0, 'msg': 'action empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def Log_page(request):
    """
    操作日志查询页面
    """
    username = request.session['username']
    add_log(username, '进入操作日志查询页面', 'Log_page')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    apis = models.operation_log.objects.values('api').distinct()
    users= models.operation_log.objects.values('user').distinct()
    api_list = []
    user_list = []
    for api in apis:
        api_list.append(api['api'])
    for user in users:
        user_list.append(user['user'])
    return render(request, 'quickit/log.html', locals())

@check_login
def Log_api(request):
    """
    操作日志查询接口
    """
    username = request.session['username']
    add_log(username, '操作日志查询', 'Log_api')
    user = request.POST.get("user")
    api = request.POST.get("api")
    date = request.POST.get("date").replace(' ','').split("-")

    start_year = int(date[0].split("/")[0])
    start_month = int(date[0].split("/")[1])
    start_day = int(date[0].split("/")[2])
    start_h = 0
    start_m = 0
    start_s = 0

    end_year = int(date[1].split("/")[0])
    end_month = int(date[1].split("/")[1])
    end_day = int(date[1].split("/")[2])
    end_h = 23
    end_m = 59
    end_s = 59

    if user == 'All':
        if api == 'All':
            logs = models.operation_log.objects.filter(date__gte=datetime.datetime(start_year,start_month,start_day,start_h,start_m,start_s),
                                                        date__lte=datetime.datetime(end_year,end_month,end_day,end_h,end_m,end_s)).order_by('-date')
        elif api != 'All' :
            logs = models.operation_log.objects.filter(api=api,
                                                       date__gte=datetime.datetime(start_year, start_month, start_day,
                                                                                   start_h, start_m, start_s),
                                                       date__lte=datetime.datetime(end_year, end_month, end_day, end_h,
                                                                                end_m, end_s)).order_by('-date')
    elif user != 'All':
        if api == 'All':
            logs = models.operation_log.objects.filter(user=user,
                                                       date__gte=datetime.datetime(start_year,start_month,start_day,start_h,start_m,start_s),
                                                        date__lte=datetime.datetime(end_year,end_month,end_day,end_h,end_m,end_s)).order_by('-date')
        elif api != 'All':
            logs = models.operation_log.objects.filter(user=user,api=api,
                                                       date__gte=datetime.datetime(start_year, start_month, start_day,
                                                                                   start_h, start_m, start_s),
                                                       date__lte=datetime.datetime(end_year, end_month, end_day, end_h,
                                                                                   end_m, end_s)).order_by('-date')

    logdata_list = []
    for log in logs:
        log_data = []
        log_data.append(str(log.date))
        log_data.append(log.user)
        log_data.append(log.operation)
        log_data.append(log.api)
        logdata_list.append(log_data)
    result = {'code': 200, 'msg': 'success','logdata':logdata_list}
    return HttpResponse(json.dumps(result), content_type="application/json")

def bug_monitor_api(request):
    '''
    获取bug信息
    '''
    data = models.BugMonitor.objects.all().order_by('-id')
    bugdata_list = []
    for bug in data:
        bug_data = []
        bug_data.append(bug.nickname)
        bug_data.append(bug.project)
        bug_data.append(bug.bugs)
        bug_data.append(str(bug.ctime))
        bugdata_list.append(bug_data)
    result = {'status': 1, 'result': bugdata_list}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def save_bi_actions(request):
    username = request.session['username']
    actions = request.POST.get("actions")
    anm = request.POST.get("anm")
    did = request.POST.get("did")
    ver = request.POST.get("ver")
    ext = request.POST.get("ext")

    utime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    has_actions = models.Bi_Actions.objects.filter(username=username,anm=anm)
    if ext =='last_select':
        models.Bi_Actions.objects.filter(username=username,ext=ext).update(ext='')
    if has_actions:
        models.Bi_Actions.objects.filter(username=username,anm=anm).update(actions=actions,utime=utime,did=did,ver=ver,ext=ext)
    else:
        insert_actions = models.Bi_Actions(username=username, actions=actions, utime=utime,anm=anm,did=did,ver=ver,ext=ext)
        insert_actions.save()
    result = {'status': 1}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def get_bi_actions(request):
    ext = request.POST.get("ext")
    username = request.session['username']
    anm = request.POST.get("anm")
    if ext == 'last_select':
        action_data = models.Bi_Actions.objects.filter(username=username, ext=ext)
        if len(action_data) !=0:
            anm = action_data[0].anm
        else:
            anm = 'utranit'
    else:
        ext = ''
        action_data = models.Bi_Actions.objects.filter(username= username,anm= anm)
    if len(action_data) != 0:
        actions = action_data[0].actions
        did = action_data[0].did
        ver = action_data[0].ver
        action_list = actions.split(",")
    else:
        did = ''
        ver = ''
        action_list = ''
    result = {'status': 1, 'action_list': action_list, 'did': did, 'ver': ver,'anm':anm}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def check_actions(request):
    username = request.session['username']
    anm = request.POST.get("anm")
    did = request.POST.get("did")
    version = request.POST.get("ver")
    date = request.POST.get("date").replace(' ','').split("/")
    start_year = int(date[0].split("-")[0])
    start_month = int(date[0].split("-")[1])
    start_day = int(date[0].split("-")[2])
    start_h = 0
    start_m = 0
    start_s = 0

    end_year = int(date[1].split("-")[0])
    end_month = int(date[1].split("-")[1])
    end_day = int(date[1].split("-")[2])
    end_h = 23
    end_m = 59
    end_s = 59

    actions = models.Bi_Actions.objects.filter(username=username,anm=anm).values("actions").first()['actions']
    action_list = actions.split(",")
    i = 0
    result_list = []
    for action in action_list:
        result_data = {}
        if did == '' and version != '':
            sql_data = models.Server_applog.objects.filter(anm=anm, action=action, ver=version,
                                                           logtime__gte=datetime.datetime(start_year, start_month,
                                                                                          start_day, start_h, start_m,
                                                                                          start_s),
                                                           logtime__lte=datetime.datetime(end_year, end_month, end_day,
                                                                                          end_h, end_m, end_s)).exists()
        elif did != '' and version == '':
            sql_data = models.Server_applog.objects.filter(anm=anm, action=action,did=did,
                                                           logtime__gte=datetime.datetime(start_year, start_month,
                                                                                          start_day, start_h, start_m,
                                                                                          start_s),
                                                           logtime__lte=datetime.datetime(end_year, end_month, end_day,
                                                                                          end_h, end_m, end_s)).exists()
        elif did == '' and version == '':
            sql_data = models.Server_applog.objects.filter(anm=anm, action=action,
                                                           logtime__gte=datetime.datetime(start_year, start_month,
                                                                                          start_day, start_h, start_m,
                                                                                          start_s),
                                                           logtime__lte=datetime.datetime(end_year, end_month, end_day,
                                                                                          end_h, end_m, end_s)).exists()
        else:
            sql_data = models.Server_applog.objects.filter(anm=anm, did=did, action=action, ver=version,
                                                logtime__gte=datetime.datetime(start_year, start_month, start_day,
                                                                               start_h, start_m, start_s),
                                                logtime__lte=datetime.datetime(end_year, end_month, end_day, end_h,
                                                                              end_m, end_s)).exists()
        if sql_data:
            result_data["status"] = 1
        else:
            result_data["status"] = 0
        result_data["action"] = action
        result_data["id"] = i
        i = i + 1
        result_list.append(result_data)
    result = {'status': 1, 'result': result_list}
    return HttpResponse(json.dumps(result), content_type="application/json")


def app_debug(request):
    '''
    app debug开关控制
    '''
    if request.method=="POST":
        project  = request.POST.get("project")
    else:
        project = request.GET.get("project")

    if project:
        debug = models.app_debug.objects.filter(project=project).values("debug").first()['debug']
        result = {'status': 1, 'debug':debug}
    else:
        result = {'status': 0, 'msg': 'project  empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")


def login_test(request):
    '''
    登陆调试
    '''
    if request.method=="POST":
        data  = request.POST.get("data")
    else:
        data = request.GET.get("data")

    if data:
        decode_data = commonFunc.decode(data)
        result = {'data': decode_data}
    else:
        result = {'status': 0, 'msg': 'data  empty'}
    return HttpResponse(json.dumps(result), content_type="application/json")

def jira(request):
    '''
    报bug
    '''
    jira_server = 'http://bug.flatincbr.com:8283'  # jira地址
    jira_username = 'Flat'  # 用户名
    jira_password = 'flat175246'  # 密码
    jira = JIRA(basic_auth=(jira_username, jira_password), options={'server': jira_server})
    if request.method=="POST":
        project = request.POST.get("project")
        title = request.POST.get("title")
        file_path = request.POST.get("file_path")
        assignee = request.POST.get("assignee")
        fixversions = request.POST.get("fixversions")
        nickname = request.POST.get("nickname")

    else:
        project = request.GET.get("project")
        title = request.GET.get("title")
        file_path = request.GET.get("file_path")
        assignee = request.GET.get("assignee")
        fixversions = request.GET.get("fixversions")
        nickname = request.GET.get("nickname")

    add_log(nickname,'创建jira:%s'%title,'jira')
    get_info = models.ding_jira.objects.filter(project=project)
    if get_info:
        project = get_info.values("jira_id").first()['jira_id']
        if assignee == '':
            assignee = get_info.values("assignee").first()['assignee']
    if project and title :
        try:
            if file_path:
                url = "http://161.117.69.170:81/upload_file"
                files = {'file': open(file_path, 'rb')}
                response = requests.post(url, files=files)
                Data = json.loads(response.text)
                file_path = Data['data']['url']
                jira.create_issue(project=str(project), summary= str(title),
                                  description=str(title) + "\n" + str(file_path),
                                  issuetype={'name': 'BUG'})
            else:
                jira.create_issue(project=str(project), summary= str(title),
                                  description=str(title),assignee={'name':assignee},
                                  issuetype={'name': 'BUG'},fixVersions=[{'name':fixversions}])
            result = {'status': 1}
            return HttpResponse(json.dumps(result), content_type="application/json")
        except Exception as e:
            result = {'status': 0,'error':str(traceback.format_exc())}
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'status': 0,'msg':'no project or title'}
        return HttpResponse(json.dumps(result), content_type="application/json")


def get_apk_url(request):
    project = request.GET.get("project")
    get_info = models.ding_pkgname.objects.filter(project=project)
    if len(get_info) != 0:
        pkgname = get_info.values('pkgname').first()['pkgname']
        url = 'http://cms.flatincbr.com:8000/api/app-version/get-apk-url'
        par = {}
        par["pkg_name"] = pkgname
        par["online"] = 1
        par["orderBy"] = "id"
        par["sortType"] = "DESC"
        par['page_size'] = 1
        req = requests.get(url=url, params=par, verify=False)
        data = req.json()
        if len(data['data']) != 0:
            download_url = data['data'][0]['url']
            version = data['data'][0]['version']
            result = {'status':1,'msg':'success','url':download_url,'version':version,'pkg_name':pkgname}
        else:
            result = {'status': 0, 'msg': '没有找到包名为%s的online正式包'%pkgname}
    else:
        result = {'status': -1, 'msg': '%s项目还没有接入，无法获取安装包链接' % project}
    return HttpResponse(json.dumps(result), content_type="application/json")

def get_ding_key(request):
    content = request.GET.get("content").lower()
    all_data = models.ding_key_msg.objects.all()
    key_msg_dict = {}
    sort_dict = {}
    '''组装分类和关键词两个dict'''
    for data in all_data:
        key_msg_dict[data.key] = {'msg':data.msg,'pic_url':data.pic_url,'pic_top':data.pic_top}
        if data.sort not in sort_dict.keys():
            sort_dict[data.sort] = []
        sort_dict[data.sort].append(data.key)
    '''遍历分类'''
    sort_list = []
    for sort_key in sort_dict:
        if sort_key in content:
            sort_list.append(sort_key)
    if len(sort_list) > 1:
        result = {"msgtype": "text", "text": {"content": '请输入你想要咨询的业务分类：\n  >  ' + "\n  >  ".join(sort_list)}}
    elif len(sort_list) == 1:
        result = {"msgtype": "text", "text": {"content": '请输入你想要咨询的具体业务：\n  >  ' + "\n  >  ".join(sort_dict[sort_list[0]])}}
    else:
        '''遍历key'''
        key_list = []
        precise = False
        for key in key_msg_dict:
            if content in key or key in content:
                if content == key:
                    precise = True
                key_list.append(key)

        if len(key_list) > 1:
            if precise == True:
                '''精准命中的词'''
                msg = key_msg_dict[content]['msg']
                pic_url = key_msg_dict[content]['pic_url']
                pic_top = key_msg_dict[content]['pic_top']
                key_list.remove(content)
                if pic_url != None:
                    msg = msg.replace(r"\n", '\n')
                    if pic_top != '1':
                        result = {"msgtype": "markdown",
                                  "markdown": {"title": msg, "text": msg + '![screenshot](%s)' % pic_url+ "\n\n" + '猜你想问其他：\n  > ' + "\n  > ".join(key_list)}}
                    else:
                        result = {"msgtype": "markdown",
                                  "markdown": {"title": msg, "text": '![screenshot](%s)' % pic_url  +  "\n\n" + '猜你想问其他：\n > ' + "\n  > ".join(key_list)}}
                else:
                    result = {"msgtype": "text", "text": {"content": msg + "\n\n" + '猜你想问其他：\n  > ' + "\n  > ".join(key_list)}}
            else:
                result = {"msgtype": "text", "text": {"content": '请输入你想要咨询的具体业务：\n  > ' + "\n  > ".join(key_list)}}

        elif len(key_list) == 1:
            msg = key_msg_dict[key_list[0]]['msg']
            pic_url = key_msg_dict[key_list[0]]['pic_url']
            pic_top = key_msg_dict[key_list[0]]['pic_top']
            if pic_url != None:
                msg = msg.replace(r"\n", '\n')
                if pic_top != '1':
                    result = {"msgtype": "markdown", "markdown": {"title": msg, "text": msg  + '![screenshot](%s)'%pic_url}}
                else:
                    result = {"msgtype": "markdown","markdown": {"title": msg, "text": '![screenshot](%s)'%pic_url +"\n"+ msg}}
                print(result)
            else:
                result = {"msgtype": "text", "text": {"content": msg}}
        else:
            print(list(sort_dict.keys()))
            result = {"msgtype": "text", "text": {"content":"没有查询到该业务，请输入以下命令：\n > #打包\n > #bug\n > 地址\n > " +  "\n > ".join(list(sort_dict.keys()))}}

    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def online_log_search(request):
    username = request.session['username']
    add_log(username, '用户查询线上日志', 'online_log_search')
    action = request.POST.get("Action")
    anm = request.POST.get("Anm")
    subanm = request.POST.get("Subanm")
    cha = request.POST.get("Cha")
    did = request.POST.get("did")
    date = request.POST.get("date")
    Date_list = str(date).split(' - ')
    startDate = Date_list[0].replace('/','')
    endDate = Date_list[1].replace('/','')
    anms = models.User.objects.filter(username=username).values("anm").first()['anm']
    anms_list = anms.split(",")
    if anm in anms_list:
        url = "http://47.74.249.92:8080//datadigger_web/api/dataapi/actionLog"
        request_data = '{"action": "%s",' \
                       '"anm": "%s",' \
                       '"cha": "%s",' \
                       '"subanm": "%s",' \
                       '"did": "%s",' \
                       '"endDate": "%s",' \
                       '"password": "denglongchuan",' \
                       '"startDate": "%s",' \
                       '"uid": "","userName": "denglongchuan"}'%(action,anm,cha,subanm,did,endDate,startDate)
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            r = json.loads(requests.post(url, headers=headers, data=request_data).text.replace(r"\\", ""))
            if r['isSuccess']:
                data_list = r['data']['records']
                # 修改data list
                for data in data_list:
                    del data[0]
                    del data[2]
                result = {'code': 200, 'msg': 'success', 'data_list': data_list}
            else:
                if r['code'] == -1:
                    result= {'code': 202, 'msg': 'max connect'}
                else:
                    result= {'code': 202, 'msg': 'unknown error'}
        except:
            result= {'code': 202, 'msg': 'unknown error'}
    else:
        result = {'code': 202, 'msg': 'Error，anm permission denied'}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def online_log_page(request):
    """
    线上用户日志查询页面
    """
    username = request.session['username']
    add_log(username, '进入线上用户日志查询页面', 'online_log')
    nickname = request.session['nickname']
    admin_type = models.User.objects.filter(username=username).values("admin_type").first()['admin_type']
    anms = models.User.objects.filter(username=username).values("anm").first()['anm']
    if anms ==None or anms == '':
        return redirect('/dashboard/')
    else:
        anms_list = anms.split(',')
        return render(request, 'quickit/online_log.html', locals())


def add_log_api(request):
    '''
    协助钉钉机器人统计
    :param request:
    :return:
    '''
    username = request.GET.get('username')
    content = request.GET.get('content')
    api = request.GET.get('api')
    add_log(username,content,api)
    result = {'code': 200, 'msg': 'success'}
    return HttpResponse(json.dumps(result), content_type="application/json")


@check_login
def app_debug_page(request):
    """
    应用debug模式控制页面
    """
    username = request.session['username']
    add_log(username, '应用debug模式控制页面', 'app_debug_page')
    nickname = request.session['nickname']
    project = models.app_debug.objects.all()
    result = {}
    anms = models.User.objects.filter(username=username).values("anm").first()['anm']
    anms_list = anms.split(',')
    for p in project:
        if p.project in anms_list:
            result[p.project] = p.debug
    return render(request, 'quickit/app_debug.html', locals())


@check_login
def app_debug_api(request):
    anm = request.GET.get('anm')
    debug = request.GET.get('status')
    username = request.session['username']
    add_log(username, 'app_debug-设置%s为%s'%(anm,debug), 'app_debug_page')
    models.app_debug.objects.filter(project=anm).update(debug=debug)
    result = {'code': 200, 'msg': 'success'}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_login
def app_debug_add_anm(request):
    username = request.session['username']
    new_anm = request.GET.get('anm')
    anms = models.app_debug.objects.values('project').distinct()
    anm_list = []
    for anm in anms:
        anm_list.append(anm['project'])
    if new_anm in anm_list:
        result = {'code': 202, 'msg': 'anm 已存在'}
    else:
        insert_anm = models.app_debug(project=new_anm, debug=0)
        insert_anm.save()
        old_anms = models.User.objects.filter(username=username).values("anm").first()['anm']
        if old_anms == '':
            new_anms = new_anm
        else:
            new_anms = old_anms + ',' + new_anm
        models.User.objects.filter(username=username).update(anm=new_anms)
        result = {'code': 200, 'msg': '添加成功'}
        add_log(username, 'app_debug-添加%s' % (new_anm), 'app_debug_page')
    return HttpResponse(json.dumps(result), content_type="application/json")

