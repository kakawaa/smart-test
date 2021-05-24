# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    nickname = models.CharField(max_length=32,default='')
    super_admin = models.BooleanField(default=False)
    admin_type = models.CharField(max_length=32,default='')
    anm = models.TextField(null=True)
    def __str__(self):
        return ' %s' % ( self.username)


class Apk(models.Model):
    id = models.AutoField(primary_key=True)                     # 自增id
    build_num = models.TextField()                              # 构建号
    package_name = models.TextField()                           # 包名/项目名称
    apk_name = models.CharField(unique=True,max_length=255)                               # 安装包名称（唯一）
    version = models.TextField()                              # 版本号
    version_code = models.TextField()                              # 版本号code
    size = models.TextField()                              # 大小
    ctime = models.DateTimeField()                            # 创建时间
    def __str__(self):
        return ' %s' % ( self.apk_name)

class Size(models.Model):
    apk_name = models.TextField()                     # 安装包全名
    dex = models.TextField()
    so = models.TextField()
    png = models.TextField()
    xml = models.TextField()
    arsc = models.TextField()
    jar = models.TextField()
    SF = models.TextField()
    MF = models.TextField()
    kotlin_metadata = models.TextField()
    jpg = models.TextField()
    gz = models.TextField()

    gif = models.TextField(default='0')
    webp = models.TextField(default='0')
    mp4 = models.TextField(default='0')
    properties = models.TextField(default='0')
    kotlin_module = models.TextField(default='0')
    kotlin_builtins = models.TextField(default='0')


    def __str__(self):
        return ' %s' % ( self.apk_name)

class Ad_sample_info(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    source_name = models.TextField()
    country = models.TextField()
    ip = models.TextField()
    gaid = models.TextField()
    ad_size = models.TextField()
    title = models.TextField()
    desc_str = models.TextField()
    image_url = models.TextField()
    click_url = models.TextField()
    request_time = models.DateTimeField()
    dt = models.DateField()
    is_html = models.TextField()
    html_str = models.TextField()
    dsp_or_ssp = models.TextField()
    creative_id = models.TextField()

    def __str__(self):
        return ' %s' % ( self.source_name)

class Ad_sample_stat(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    dt = models.DateField()
    source_name = models.TextField()
    loc = models.TextField()
    req = models.IntegerField()
    suc = models.IntegerField()
    fail = models.IntegerField()

    def __str__(self):
        return ' %s' % ( self.source_name)

class StartUpTime(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    pkgname = models.TextField()
    version = models.TextField()
    scene = models.TextField(default='') #损耗时间类型
    timecost = models.IntegerField(default=0) #损耗时间
    time_detail = models.TextField(default='')  # 详细耗时数据
    status = models.TextField(default='Offline')  # 状态
    ctime = models.DateTimeField()

    def __str__(self):
        return ' %s' % ( self.apkname)

class Performance(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    pkgname = models.TextField()
    version = models.TextField()
    logname = models.TextField()
    scene = models.TextField(default='')
    status = models.TextField(default='Offline')  # 状态
    ctime = models.DateTimeField()

    def __str__(self):
        return ' %s' % ( self.apkname)

class Applog(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    pkgname = models.TextField()
    version = models.TextField()
    logname = models.TextField()
    remark = models.TextField()
    did = models.TextField(default='')
    app_config = models.TextField(default='')
    mediation_config = models.TextField(default='')
    ctime = models.DateTimeField()

    def __str__(self):
        return ' %s' % ( self.logname)

class APImoitor(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    project = models.TextField()
    api = models.TextField()
    errortimes = models.IntegerField()
    errortype = models.TextField()
    datetime = models.TextField(default='')
    ctime = models.DateTimeField()

    def __str__(self):
        return ' %s' % ( self.api)


class APIinfo(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    project = models.TextField()
    env = models.TextField()
    api = models.TextField(default='')
    url = models.TextField(null=True)
    request_name = models.TextField(default='{}')
    response_name = models.TextField(default='{}')
    ctime = models.DateTimeField()
    status = models.TextField(default='Online')

    def __str__(self):
        return ' %s' % ( self.api)

class APItask(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    project = models.TextField()
    env = models.TextField()
    taskname = models.TextField()
    creater = models.TextField()
    ctime = models.DateTimeField()

    timercheck = models.TextField(default='')
    timevalue = models.IntegerField(default=0)
    timetype = models.TextField(default='')
    case = models.TextField(default='NA')

    status = models.TextField(default='None')

    def __str__(self):
        return ' %s' % ( self.taskname)

class APIcase(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    project = models.TextField()
    env = models.TextField()
    api = models.TextField()
    taskname = models.TextField()
    creater = models.TextField()
    check_data = models.TextField()
    ctime = models.DateTimeField()

    def __str__(self):
        return ' %s' % ( self.taskname)

class Taskresult(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    project = models.TextField()
    env = models.TextField()
    taskname = models.TextField()
    status = models.TextField()
    result = models.TextField()
    ctime = models.DateTimeField()

    errorcount = models.IntegerField(default=0)
    passcount = models.IntegerField(default=0)

    def __str__(self):
        return ' %s' % ( self.taskname)




class Server_applog(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    project = models.TextField()     #项目
    anm = models.TextField(default='') #anm
    subanm = models.TextField(default='') #subanm
    action = models.TextField(default='') #action
    cha = models.TextField(default='')  # 渠道
    ver = models.TextField(default='')  # 版本
    type = models.TextField(default='')#活动类型
    did =  models.TextField(default='')#did
    brd = models.TextField(default='')  # 手机信息
    logcontent = models.TextField()  #日志内容
    logtime = models.DateTimeField() #日志时间
    def __str__(self):
        return ' %s' % ( self.id)

class operation_log(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    date = models.DateTimeField()
    user = models.TextField()
    operation = models.TextField()
    api = models.TextField()

    def __str__(self):
        return ' %s' % ( self.operation)

class BugMonitor(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    nickname = models.TextField()
    project = models.TextField()
    bugs = models.IntegerField()
    ctime = models.DateTimeField()
    def __str__(self):
        return ' %s' % ( self.nickname)


class Bi_Actions(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    username = models.TextField()
    actions = models.TextField()
    utime = models.DateTimeField()
    anm = models.TextField(default='')
    did = models.TextField(default='')
    ver = models.TextField(default='')
    ext = models.TextField(default='')
    def __str__(self):
        return ' %s' % ( self.username)


class app_debug(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    project = models.TextField()
    debug = models.IntegerField()
    def __str__(self):
        return ' %s' % ( self.username)

class jmeter_data(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    build_num = models.TextField(default='')
    simpleNum = models.TextField(default='')
    avg = models.TextField(default='')
    median = models.TextField(default='')
    percent90 = models.TextField(default='')
    percent95 = models.TextField(default='')
    percent99 = models.TextField(default='')
    min = models.TextField(default='')
    max = models.TextField(default='')
    error = models.TextField(default='')
    throughput = models.TextField(default='')
    send = models.TextField(default='')
    url = models.TextField(default='')
    params = models.TextField(default='')
    treadNum = models.TextField(default='')
    loopNum = models.TextField(default='')
    rampUp = models.TextField(default='')

class ding_build_apk(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    anm = models.TextField()
    env = models.TextField(default='debug')
    jobname = models.TextField()
    parameters = models.TextField(default='')

class ding_jira(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    project = models.TextField()
    jira_id = models.TextField()
    assignee = models.TextField()

class ding_key_msg(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    key = models.TextField()
    msg = models.TextField()
    pic_url = models.TextField()
    pic_top = models.TextField()
    sort = models.TextField(default='基建')

class ding_pkgname(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id
    project = models.TextField()
    pkgname = models.TextField()


class service_manager(models.Model):
    '''
    服务管理
    '''
    id = models.AutoField(primary_key=True)
    service = models.TextField()
    status = models.TextField(default='')
    operate = models.TextField(default='')
    dtime = models.DateTimeField()
    def __str__(self):
        return ' %s' % ( self.id)