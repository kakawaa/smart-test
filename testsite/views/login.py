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

class Login(View):

    @classmethod
    def login_page(cls,request):
        return render(request, 'elver/login/sign-in.html')


    @classmethod
    @method_decorator(Decorators.catch_except)
    def login_api(cls,request):
        """账号密码登录"""
        username = common.request_method(request,'username')
        password = common.request_method(request,'password')
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
            request.session['nickname'] = nickname
            result = {'code': 200, 'msg': 'old password wrong!'}
        else:
            result = {'code': 202, 'msg': 'old password wrong!'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def sign_up_page(cls, request):
        """账号注册页面"""
        return render(request, 'elver/login/sign-up.html')

    @classmethod
    @method_decorator(Decorators.catch_except)
    def sign_up_api(cls, request):
        """账号注册api"""
        username = common.request_method(request, 'username')
        password = common.request_method(request, 'password')
        user = models.User.objects.filter(username=username, password=password)
        if user:
            result = {'code': 202, 'msg': '账号已经存在'}
        else:
            models.User(username=username, password=password,nickname=username).save()
            result = {'code': 200, 'msg': '创建账号成功'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def logout(cls,request):
        """退出登录"""
        auth.logout(request)
        response = redirect('/login/signin')
        return response

    @classmethod
    @method_decorator(Decorators.catch_except)
    def scan_login(cls, request):
        """钉钉登录"""
        # 修改为后端请求钉钉url
        ding_url = request.POST.get('ding_url')
        result = requests.get(ding_url)
        request.session['is_login'] = '1'
        request.session['username'] = result.json()['username']
        request.session['nickname'] = result.json()['nickname']
        return HttpResponse(json.dumps(result.json()), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def scan_login_api(cls, request):
        """二维码认证接口"""
        if request.method == "GET":
            code = request.GET.get('code', )
            appId = 'dingoabey3yfj0iyxvkvn3'
            appSecret = 'rmdjih3UDXXqPwJ7q1VpnGKL2P_wRNaxnAzgszwH8D1JVxWCBnM0hF9BqCCYIrhI'

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
                "https://oapi.dingtalk.com/sns/get_sns_token?access_token={access_token}".format(
                    access_token=access_token),
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
                'https://oapi.dingtalk.com/gettoken?appkey={appkey}&appsecret={appsecret}'.format(appkey=appid_new,
                                                                                                  appsecret=appSecret_new))
            user_id_reponse = requests.get(
                'https://oapi.dingtalk.com/user/getUseridByUnionid?access_token={user_token}&unionid={unionid}'.format(
                    user_token=user_token.json()['access_token'],
                    unionid=user_info['unionid']))
            errcode = user_id_reponse.json()['errcode']
            # errcode=0代表用户存在
            if errcode == 0:
                # 用户存在于企业，并可以获取到id，就通过id查询详细信息
                userid = user_id_reponse.json()['userid']
                user_info = requests.post(
                    "https://oapi.dingtalk.com/topapi/v2/user/get?access_token={access_token}".format(
                        access_token=user_token.json()['access_token']),
                    json={
                        "userid": userid,
                        "language": 'zh_CN'
                    })
                all_user_info = user_info.json()
                avatar = all_user_info['result']['avatar']
                if avatar is None:
                    avatar = "https://v.xxxx.mobi/d4/pic/cms/xxxx/1641182134932.png?t=1641182135057"
                mobile = all_user_info['result']['mobile']
                name = all_user_info['result']['name']
                # 安全起见 不用userid，使用unionid
                unionid = all_user_info['result']['unionid']
                is_user = models.User.objects.filter(token=unionid)
                # is_user = models.User.objects.filter(username=name)
                if not is_user:
                    models.User(username=name, password='dfajSUmLT#y#iOT8r6%20pk&', super_admin=0,
                                nickname=name, avatar=avatar, mobile=mobile, token=unionid,
                                admin_type=0).save()
                else:
                    models.User.objects.filter(token=unionid).update(username=name, nickname=name, mobile=mobile,avatar=avatar)
                result = {'code': 200, 'msg': 'login suc!', 'nickname': name, 'username': name}
            else:
                result = {'code': 202, 'msg': 'login wrong!', 'nickname': '', 'username': ''}
        return HttpResponse(json.dumps(result), content_type="application/json")