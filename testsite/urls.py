# -*- coding:utf-8 -*-
from django.urls import path
from django.urls import include
from testsite.views.login import *
from testsite.views.builder import *
from testsite.views.apk import *
from testsite.views.setting import *


app_name = 'testsite'

urlpatterns = [

    path('',Builder.builder_page),

    #【Login】
    path('login/', Login.login_page, name='login_page'),
    path('login_api/', Login.login_api, name='login_api '),
    path('sign_up/', Login.sign_up_page, name='sign_up_page '),
    path('sign_up_api/', Login.sign_up_api, name='sign_up_api '),
    path('logout/', Login.logout, name='logout'),

    #【Setting】
    path('setting/', Setting.setting_page, name='setting_page'),

    #【Builder】
    path('builder/', Builder.builder_page, name='builder_page'),
    path('builder_detail/', Builder.builder_detail_page, name='builder_detail_page'),
    path('builder_step/', Builder.builder_step_page, name='builder_step_page'),

    #【APK】
    path('apk/', APK.apk_page, name='apk_page'),
    path('get_apk_info_api/', APK.get_apk_info_api, name='get_apk_info_api'),
]
