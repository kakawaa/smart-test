import datetime
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
                    # 失败重试一次
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
    def decode_file(cls,value, path, file_type):
        """bs64解密保存文件"""
        if (len(value) % 4 == 1):
            value += "=="
        elif (len(value) % 4 == 2):
            value += "="
        bs = base64.b64decode(value)
        fh = open(path + '/'+str(time.strftime("%Y%m%d%H%M%S", time.localtime())) + "." + file_type, "wb")
        fh.write(bs)
        fh.close()
        filepath = f'http://47.106.194.167:8181/ti/{file_type}/{str(time.strftime("%Y%m%d%H%M%S", time.localtime()))}.{file_type}'
        filename = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "." + file_type
        if file_type.__contains__('json'):
            os.chdir(path)
            cls.putcmd(f'python3 statistics.py {filename}')
        return filepath,filename


    @classmethod
    def mysql_connect(cls,host,user,password,table):
        """mysql连接"""
        db = MySQLdb.connect(host, user, password,table, charset='utf8')
        cursor = db.cursor()
        return cursor,db