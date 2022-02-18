# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
import os
from django.views import View
from django.utils.decorators import method_decorator
from django.template.defaultfilters import filesizeformat
from django.utils import timezone
from django.contrib import auth
import json
from testsite import models
from testsite.public.common import common
from testsite.public.decorators import Decorators
from django.http import HttpResponse
import time
import shutil
import requests
import sys
sys.getdefaultencoding()

common = common()

class File(View):

    st_file_path = '/home1/www/tomcat/apache-tomcat-9.0.27/webapps/examples/stest/file/'
    #st_file_path = '/Users/chenhongqing/Documents/code/smart-test/file/'

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def directory_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        directorys = models.DirectoryInfo.objects.all().order_by('-id')
        directory_names = models.DirectoryInfo.objects.all().order_by('-id').values('directory_name').distinct()
        directory_num = models.DirectoryInfo.objects.all().count()
        return render(request, 'elver/file/directory.html',locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def file_page(cls,request,*arg,**kwargs):
        directory = kwargs['directory']
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        files = models.DirectoryFile.objects.filter(directory_name=directory).order_by('-id')
        file_names = models.DirectoryFile.objects.filter(directory_name=directory).order_by('-id').values('file_name').distinct()
        file_num = models.DirectoryFile.objects.filter(directory_name=directory).count()
        return render(request, 'elver/file/file.html',locals())

    @classmethod
    @method_decorator(Decorators.catch_except)
    def create_directory_api(cls, request):
        """创建文件夹接口"""
        directory_name = common.request_method(request, "directory_name")
        creater = common.request_method(request, "creater")
        directory_num = models.DirectoryInfo.objects.filter(directory_name=directory_name).count()
        if directory_num == 0:
            directory_name = str(directory_name).replace(' ','').replace('/','').replace('&','').strip()
            models.DirectoryInfo(directory_name=directory_name, creater=creater).save()
            if not os.path.exists(cls.st_file_path + directory_name):
                os.mkdir(cls.st_file_path + directory_name)
            result = {'status': 1, 'msg': '创建文件夹成功'}
        else:
            result = {'status': 0, 'msg': '该文件夹已存在'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def edit_directory_api(cls, request):
        """编辑文件夹信息接口"""
        old_directory_name = common.request_method(request, "old_directory_name")
        new_directory_name = common.request_method(request, "new_directory_name")
        ctime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        try:
            if old_directory_name != new_directory_name or new_directory_name:
                directory_num = models.DirectoryInfo.objects.filter(directory_name=new_directory_name).count()
                if directory_num == 0:
                    models.DirectoryInfo.objects.filter(directory_name=old_directory_name).update(directory_name=new_directory_name,ctime=ctime)
                    models.DirectoryFile.objects.filter(directory_name=old_directory_name).update(directory_name=new_directory_name,ctime=ctime)
                    if not os.path.exists(cls.st_file_path + new_directory_name):
                        os.rename(cls.st_file_path + old_directory_name,cls.st_file_path + new_directory_name)
                    result = {'status': 1, 'msg': '更新成功！'}
                else:
                    result = {'status': 0, 'msg': '该文件夹名称已经被使用'}
            else:
                result = {'status': 0, 'msg': '命名没有变化或为空'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def delete_directory_api(cls, request):
        """删除文件夹接口"""
        directory_name = common.request_method(request, "directory_name")
        owner = common.request_method(request, "owner")
        directory_owner = models.DirectoryInfo.objects.filter(directory_name=directory_name).values("creater").last()['creater']
        file_num = models.DirectoryFile.objects.filter(directory_name=directory_name).count()
        if owner == directory_owner:
            if file_num == 0:
                models.DirectoryInfo.objects.filter(directory_name=directory_name).delete()
                models.DirectoryFile.objects.filter(directory_name=directory_name).delete()
                if os.path.exists(cls.st_file_path + directory_name):
                    os.removedirs(cls.st_file_path + directory_name)
                result = {'status': 1, 'msg': '删除成功！'}
            else:
                result = {'status': 0, 'msg': '文件个数>0,请先删除文件记录'}
        else:
            result = {'status': 0, 'msg': '不是OWNER,无法操作!'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    
    @classmethod
    @method_decorator(Decorators.catch_except)
    def upload_file_api(cls,request):
        """上传文件"""
        file_name = request.POST.get('file_name')
        directory = request.POST.get('directory')
        file_size = request.POST.get('file_size')
        creater = request.POST.get('creater')
        file_obj = request.FILES.get('file')
        file_path = cls.st_file_path + directory
        splitext = os.path.splitext(file_name)[-1][1:]
        ctime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        file_name = common.replace_name(file_name)
        if splitext in ['mp4','mkv','mov','MOV','webm','flv','avi','3gp','3gp2','mpg','ts','m4v','mpeg','vob','asf','wmv']:
            file_type = 'video'
        elif splitext in ['zip','rar','gz']:
            file_type = 'zip'
        elif splitext in ['png','svg','jpg','webp','bmp','jpeg']:
            file_type = 'image'     
        else:
            file_type = 'other'    
        try:
            file_num = models.DirectoryFile.objects.filter(directory_name=directory,file_name=file_name).count()
            if file_num == 0:
                if not os.path.exists(file_path):
                    os.mkdir(file_path)
                with open(f'{file_path}/{file_name}', 'wb+') as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)
            else:
                result = {'status': 0,'msg': '该文件已经存在'}
                return HttpResponse(json.dumps(result), content_type="application/json")
        except Exception as e:
            result = {'status': 0, 'msg': f'上传失败:{str(e)}','error':str(e)}
        else:
            file_size = filesizeformat(int(file_size))
            fileurl = f'http://47.106.194.167:8181/stest/file/{directory}/{file_name}'
            models.DirectoryFile(directory_name=directory,file_name=file_name,file_type=file_type,
                                 file_size=file_size,file_link=fileurl,creater=creater).save()
            file_num = models.DirectoryFile.objects.filter(directory_name=directory).count()
            models.DirectoryInfo.objects.filter(directory_name=directory).update(file_num=file_num,ctime=ctime)
            result = {'status': 1, 'fileurl': fileurl, 'msg': 'upload success'}
        return HttpResponse(json.dumps(result), content_type="application/json")   

    @classmethod
    @method_decorator(Decorators.catch_except)
    def delete_directory_file_api(cls, request):
        """删除文件接口"""
        directory_name = common.request_method(request, "directory_name")
        file_name = common.request_method(request, "file_name")
        creater = common.request_method(request, "creater")
        ctime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        file_owner = models.DirectoryFile.objects.filter(directory_name=directory_name,file_name=file_name).values("creater").last()['creater']
        if creater == file_owner:
            models.DirectoryFile.objects.filter(directory_name=directory_name,file_name=file_name).delete()
            file_num = models.DirectoryFile.objects.filter(directory_name=directory_name).count()
            models.DirectoryInfo.objects.filter(directory_name=directory_name).update(file_num=file_num,ctime=ctime)
            os.remove(cls.st_file_path+directory_name+'/'+file_name)
            result = {'status': 1, 'msg': '删除成功！'}
        else:
            result = {'status': 0, 'msg': '不是OWNER,无法操作!'}
        return HttpResponse(json.dumps(result), content_type="application/json")     