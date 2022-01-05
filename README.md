<p align="center">
<a href="#"><img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1641353107161-276431b1-c3d2-48a7-b4d1-fea96c68858d.png" alt="Elver" width="300"></a><br><br>
</p>
<p align="center">
<a href="#" target="__blank"><img src="https://img.shields.io/static/v1?label=Demo&message=preview&color=228be6" alt="SmartTest preview"></a>
<br>
</p>

## 简介

智测云是一个提供多种测试技术解决方案的质量开放平台，提供的功能服务包括CI/CD构建器、APK包检测、自动化测试、性能测试、服务监控、代码检查。

我们致力于解决低效、繁琐的测试执行，我们的目标是Simple Test In Smart Test !


## 特性

* **BUILDER:** CI/CD构建器.
* **APK:** 信息保存、资源解析、病毒扫描、安全加固.
* **API TEST:** 接口手工测试、自动化测试、压力测试.
* **SERVER:** 服务监控、异常日志回溯.
* **APM**: APP性能指标监控.
* **APP**: APP用户反馈、崩溃分析、客户端日志、埋点.
* **CODE:** 代码扫描、覆盖率.

## 界面

#### 一.登陆
<a href="http://0.0.0.0:5656/login/signin" target="_blank">
<img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1641352819682-45685d58-f217-4cb0-8fed-b5864216e9c9.png?x-oss-process=image%2Fresize%2Cw_1500%2Climit_0">
</a>

#### 二.BUILDER
<a href="http://0.0.0.0:5656/builder/home" target="_blank">
<img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1641352936661-22cff130-3ea1-443b-97ca-9305138b8280.png?x-oss-process=image%2Fresize%2Cw_1500%2Climit_0">
</a>

#### 三.APK
<a href="http://0.0.0.0:5656/apk/info" target="_blank">
<img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1641353219987-3e989a00-e6f4-4dad-be45-87eca7542ec6.png?x-oss-process=image%2Fresize%2Cw_1500%2Climit_0">
</a>

#### 四.API TEST
<a href="http://0.0.0.0:5656/apk/info" target="_blank">
<img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1641353390550-f30e206b-3f66-4736-b657-2222c76e4980.png?x-oss-process=image%2Fresize%2Cw_1500%2Climit_0">
</a>

#### 五.SERVER
<a href="http://0.0.0.0:5656/api_test/automation" target="_blank">
<img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1641353519200-4f21ccee-0a11-499c-a544-25f6e2939203.png?x-oss-process=image%2Fresize%2Cw_1500%2Climit_0">
</a>

#### 六.APM
<a href="http://0.0.0.0:5656/apm/test" target="_blank">
<img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1641353525461-7c67cbda-0a46-4a12-9ea6-65342afd488f.png?x-oss-process=image%2Fresize%2Cw_1500%2Climit_0">
</a>

#### 七.APP
<a href="http://0.0.0.0:5656/app/crash" target="_blank">
<img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1641353532268-7c6c898f-4225-477c-aebb-e6117a81a261.png?x-oss-process=image%2Fresize%2Cw_1500%2Climit_0">
</a>

## 文档

http://0.0.0.0:5656/doc/started

## 环境

1. [安装 Django 3.2.9](https://www.djangoproject.com/download/).
2. [安装 Python](https://www.python.org/downloads/) - 推荐版本 [3.9](https://www.python.org/downloads/).
3. [安装 nginx](https://nginx.org/en/download.html) 访问static里面的静态资源.
4. [安装 uwsgi](http://projects.unbit.it/downloads/uwsgi-latest.tar.gz) 启动平台服务.
5. [安装 mysql](https://dev.mysql.com/downloads/mysql/).
6. 安装依赖：
```sh
sh make_env.sh
```
7. 初始化表数据
```sh
创建数据库：smart-test
创建表：sh addtable.sh
```

## 本地运行
1. 配置数据库信息，在./mysite/setting.py
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smart-test', #数据库
        'USER': 'username', #用户名
        'PASSWORD': 'password', #密码
        'HOST': 'xx.xx.xx.xx', #装mysql的机器
        'PORT': '3306',
    }
}
```
2. 在根目录 `/elver` , 在终端执行 `sh run.sh`.
3. 浏览器打开 [http://0.0.0.0:5656](http://0.0.0.0:5656).

## 贡献人

<img style="width:100px " src="https://avatars.githubusercontent.com/u/24454096?s=400&u=50b8771dcf3b45bddb0eaef44c3dd82597cc69d4&v=4" />

