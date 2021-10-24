# -*- coding:utf-8 -*-
from django.urls import path
from testsite.views.login import *
from testsite.views.builder import *


app_name = 'testsite'

urlpatterns = [

    path('',Builder.builder_page),

    #【Login】
    path('login/', Login.login_page, name='login_page'),
    path('login_api/', Login.login_api, name='login_api '),
    path('sign_up/', Login.sign_up_page, name='sign_up_page '),
    path('sign_up_api/', Login.sign_up_api, name='sign_up_api '),
    path('logout/', Login.logout, name='logout'),

    #【Home】
    path('builder/', Builder.builder_page, name='builder_page'),
]
