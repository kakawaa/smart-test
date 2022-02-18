import datetime
from enum import Flag
from re import T
from django.db.models.expressions import F
import requests
import urllib.parse
import base64
import jenkins
import os
import json
import time
import jinja2
import shutil
from django.shortcuts import render,redirect
from testsite import models
from functools import wraps
import MySQLdb
from logzero import logger
import subprocess
from androguard.core.bytecodes.apk import APK

class common(object):

    @classmethod
    def __init__(cls):
        cls.headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0',
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }

    @classmethod
    def check_login(cls,f):
        """登录检查装饰器"""
        @wraps(f)
        def inner(request, *arg, **kwargs):
            if request.session.get('is_login') == '1':
                return f(request, *arg, **kwargs)
            else:
                return redirect('/login/')
        return inner

    @classmethod
    def request_method(cls,request,object):
        """请求方法"""
        if request.method == "POST":
            return request.POST.get(object)
        else:
            return request.GET.get(object)

    @classmethod
    def putcmd(cls,cmd):
        """执行命令函数"""
        logger.info("执行命令：" + cmd)
        cmd = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out = str(cmd.stdout.read(), encoding="utf-8")
        error = str(cmd.stderr.read(), encoding="utf-8")
        if len(out.strip()) > 0:
            if isinstance(out, list or dict):
                logger.info("命令输出为：")
                try:
                    json.dumps(out, indent=4)
                except:
                    cmd = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                    out = str(cmd.stdout.read(), encoding="utf-8")
                    error = str(cmd.stderr.read(), encoding="utf-8")
                logger.info(json.dumps(out, indent=4))
            else:
                logger.info("命令输出为：" + out)
        elif len(error.strip()) > 0:
            if isinstance(error, list or dict):
                logger.info("命令输出为：")
                logger.info(json.dumps(error, indent=4))
            else:
                logger.info("命令错误输出为：" + error)
        return out.strip(), error.strip()


    @classmethod
    def get_file_name_list(cls,file_dir):
        """
        :brief:获取文件夹下内，所有文件
        :param file_dir:文件夹目录
        :return: 文件列表
        """
        for root, dirs, files in os.walk(file_dir):
            return files
        else:
            return None

    @classmethod
    def getDatesByTimes(cls,sDateStr, eDateStr):
        """获取区间日期"""
        date_list:list
        datestart = datetime.datetime.strptime(sDateStr, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(eDateStr, '%Y-%m-%d')
        date_list.append(datestart.strftime('%Y-%m-%d'))
        while datestart < dateend:
            datestart += datetime.timedelta(days=1)
            date_list.append(datestart.strftime('%Y-%m-%d'))
        return date_list

    @classmethod
    def getTojson(cls,data):
        """get转化json请求体"""
        datalist = str(data).split('&')
        request_data_list = []
        for i in range(len(datalist)):
            datalist_value = datalist[i].split('=')
            request_data_list.append(datalist_value)
        return str(dict(request_data_list))


    @classmethod
    def decode_file(cls,value,file_path,directory,file_name):
        """bs64解密保存文件"""
        if (len(value) % 4 == 1):
            value += "=="
        elif (len(value) % 4 == 2):
            value += "="
        bs = base64.b64decode(value)
        # fh = open(f'{path}/{stime}.{file_type}', "wb")
        # fh.write(bs)
        # fh.close()
        with open(f'{file_path}/{directory}/{file_name}', 'wb+') as destination:
            # for chunk in bs.chunks():
            destination.write(bs)
        filepath = f'http://47.106.194.167:8181/stest/file/{directory}/{file_name}'
        return filepath


    @classmethod
    def mysql_connect(cls,host,user,password,table):
        """mysql连接"""
        db = MySQLdb.connect(host, user, password,table, charset='utf8')
        cursor = db.cursor()
        return cursor,db

    @classmethod
    def get_apk_info(cls,apk_path):
        """获取apk信息"""
        apk_info = {}
        androguard = APK(apk_path)
        if androguard.is_valid_APK():
            # apk_info.append(get_file_md5(apk_path))
            # apk_info.append(get_cert_md5(androguard))
            apk_info['app'] = androguard.get_app_name()
            apk_info['pkgname'] = androguard.get_package()
            apk_info['version_code'] = androguard.get_androidversion_code()
            apk_info['version_name'] = androguard.get_androidversion_name()
            apk_info['main_activity'] = androguard.get_main_activity()
        return apk_info

    @classmethod
    def case_get_post(cls, url, playload):
        """用例发送Get请求"""
        response = requests.request("POST", url, data=playload.encode('utf-8'),
                                    headers=cls.headers, verify=False,timeout=20)
        code = response.status_code
        return code, json.loads(response.text)

    @classmethod
    def case_json_post(cls,url,request):
        """用例发送Json请求"""
        playload = ''
        request = json.loads(request)
        for key in request.keys():
            playload += str(key) + "=" + str(request[key]) + "&"
        if playload.endswith("&"):
            playload = playload[:-1]
        response = requests.request("POST", url, data=playload.encode('utf-8'),
                                    headers=cls.headers,verify=False,timeout=20)
        code = response.status_code
        return code,json.loads(response.text)
    
    @classmethod
    def compare(cls,parameter,assert_type,value):
        """参数比较"""
        if assert_type == '==':
            Flag = (False,True)[str(parameter) == str(value)]
            result = {'pre':str(value),'final':str(parameter)}
        elif assert_type == '!=':
            Flag = (False,True)[str(parameter) != str(value)]
            result = {'pre':str(value),'final':str(parameter)}
        elif assert_type == '>':
            if isinstance(parameter,str):
                Flag = (False,True)[len(parameter) > int(value)]
                result = {'pre':int(value),'final':len(parameter)}
            elif isinstance(parameter,int):
                Flag = (False,True)[parameter > int(value)]
                result = {'pre':int(value),'final':parameter}
            else:
                Flag = (False,True)[len(parameter) > int(value)]    
                result = {'pre':int(value),'final':len(parameter)}
        elif assert_type == '<':
            if isinstance(parameter,str):
                Flag = (False,True)[len(parameter) < int(value)]
                result = {'pre':int(value),'final':len(parameter)}
            elif isinstance(parameter,int):
                Flag = (False,True)[parameter < int(value)]
                result = {'pre':int(value),'final':parameter}
            else:
                Flag = (False,True)[len(parameter) < int(value)]    
                result = {'pre':int(value),'final':len(parameter)}    
        return Flag,result

    @classmethod
    def assert_check(cls,**kwargs):
        """断言检查"""
        if kwargs['check_type'] == 'code':
            if kwargs['case_type'] in ['Get','Script']:
                final_value = cls.case_get_post(kwargs['url'],kwargs['playload'])[0]
                compare_result = cls.compare(final_value,kwargs['assert_type'], kwargs['value'])
                response = cls.case_get_post(kwargs['url'],kwargs['playload'])[1]
            else:
                final_value = cls.case_json_post(kwargs['url'],kwargs['playload'])[0]
                compare_result = cls.compare(final_value,kwargs['assert_type'], kwargs['value'])
                response = cls.case_json_post(kwargs['url'], kwargs['playload'])[1]
        else:
            if kwargs['case_type'] in ['Get','Script']:
                final_value = cls.case_get_post(kwargs['url'],kwargs['playload'])[1][kwargs['parameter']]
                compare_result = cls.compare(final_value,kwargs['assert_type'], kwargs['value'])
                response = cls.case_get_post(kwargs['url'], kwargs['playload'])[1]
            else:
                final_value = cls.case_json_post(kwargs['url'],kwargs['playload'])[1][kwargs['parameter']]
                compare_result = cls.compare(final_value,kwargs['assert_type'], kwargs['value'])
                response = cls.case_json_post(kwargs['url'], kwargs['playload'])[1]
        result = {'pass': compare_result[0], 'pre': compare_result[1]['pre'], 'final': compare_result[1]['final'],'response':response}
        return result

    @classmethod
    def build_jenkins_job(cls,jobname,parameter:dict):
        """构建jenkins任务"""
        server = jenkins.Jenkins('http://47.106.194.167:8081/', username='chenhq', password='chq175246')
        server.build_job(jobname,parameter)

    @classmethod
    def dingding_robot(cls, data ,dingding_robot_token):
        """发送钉钉消息"""
        headers = {'content-type': 'application/json'}
        r = requests.post(dingding_robot_token, headers=headers, data=json.dumps(data))
        r.encoding = 'utf-8'
        return (r.text)

    @classmethod
    def send_api_error_msg(cls,ding_switch,**kwargs):
        """发送api监控异常消息"""
        taskname = kwargs['taskname']
        apiname = kwargs['apiname']
        url = kwargs['url']
        casename = kwargs['casename']
        request_content = kwargs['request_content']
        response = kwargs['response']
        parameter = kwargs['parameter']
        pre_value = kwargs['pre_value']
        final_value = kwargs['final_value']
        assert_type = kwargs['assert_type']
        run_id = kwargs['run_id']
        dingding_robot_token = kwargs['dingding_robot_token']
        Data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "智测云API监控异常告警",
                "text": f"\n > #### 任务: {taskname}" \
                        + f"\n > #### 接口: {apiname}" \
                        + f"\n > #### URL: {url}" \
                        + f"\n > #### 用例: {casename}" \
                        + f"\n > #### 请求内容: {request_content}" \
                        + f"\n > #### 返回内容: {response}" \
                        + f"\n > #### 校验参数: {parameter}" \
                        + f"\n > #### 预期值: {pre_value}" \
                        + f"\n > #### 断言: {assert_type}" \
                        + f"\n > #### 实际值: {final_value}" \
                        + f"\n > #### [查看详情](http://47.106.194.167:5656/api_test/automation/{taskname}/{apiname}/result/{run_id})"
            },
            "at": {
                "atMobiles": ["13524352709"],
                "isAtAll": False
            }
        }
        if ding_switch == 'true':
            cls.dingding_robot(Data,dingding_robot_token)
    

    @classmethod
    def add_user_log(cls,username, **kwargs):
        """记录用户操作日志"""
        avatar = kwargs['avatar']
        page = kwargs['page']
        action = kwargs['action']
        content = kwargs['content']
        models.Log.objects.create(username=username,avatar=avatar,page=page,action=action,content=content)

    @classmethod
    def replace_name(cls,name):
        """去除文件名特殊字符"""
        return str(name).replace(' ', '').replace('/', '').replace('&', '').strip()

    @classmethod
    def save_upload_file(cls, file_path,file_obj):
        """保存上传文件"""
        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)