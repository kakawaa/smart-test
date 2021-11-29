# -*- coding:utf-8 -*-
from django.urls import path
from django.urls import include
from testsite.views import login
from testsite.views import builder
from testsite.views import apk
from testsite.views import user
from testsite.views import api
from testsite.views import server
from testsite.views import timeline
from testsite.views import doc
from testsite.views import apm


app_name = 'testsite'
urlpatterns = [

    path('',login.Login.login_page, name='login_page'),

    ######【Login】
    path('login/signin', login.Login.login_page, name='login_page'),
    path('login/signup', login.Login.sign_up_page, name='sign_up_page '),
    path('login_api/', login.Login.login_api, name='login_api '),
    path('sign_up_api/', login.Login.sign_up_api, name='sign_up_api '),
    path('logout/', login.Login.logout, name='logout'),

    ######【Setting】
    path('setting/profile', user.Setting.setting_page, name='setting_page'),

    ######【Activity】
    path('activity/', user.UserActivity.user_activity_page, name='user_activity_page'),

    ######【BUILDER】
    path('builder/<home_path>', builder.Builder.builder_page, name='builder_page'),
    path('builder/job/<jobname>', builder.Builder.builder_detail_page, name='builder_detail_page'),
    path('builder/job/<jobname>/<item>', builder.Builder.builder_step_page, name='builder_step_page'),

    ######【APK】
    path('apk/info', apk.INFO.apk_info_page, name='apk_info_page'),
    path('get_apk_info_api/', apk.INFO.get_apk_info_api, name='get_apk_info_api'),

    path('apk/virus_scan', apk.VIRUS_SCAN.virus_scan_page, name='virus_scan_page'),
    path('apk/reinforce', apk.REINFORCE.reinforce_page, name='reinforce_page'),

    ######【API TEST】
    path('api_test/post', api.API_POST.post_page, name='post_page'),
    path('api_test/demo', api.API_POST.demo_api, name='demo_api'),
    path('api_test/get_response_api', api.API_POST.get_response_api, name='get_response_api'),

    path('api_test/automation', api.API_TASK.task_page, name='task_page'),
    path('api_test/automation/<taskname>', api.API_TASK.task_content_page, name='task_content_page'),
    path('api_test/automation/<taskname>/<apiname>', api.API_TASK.api_case_page, name='api_case_page'),

    path('api_test/stress', api.API_STRESS_TEST.stress_test_page, name='stress_test_page'),

    ######【SERVER】
    path('server/monitor', server.MONITOR.server_monitor_page, name='server_monitor_page'),
    path('server/log', server.LOG.server_log_page, name='server_log_page'),

    ######【TIMELINE】
    path('timeline/', timeline.Timeline.timeline_page, name='timeline_page'),

    ######【DOCUMENT】
    path('doc/<path>', doc.Document.document_page, name='document_page'),

    ######【APM】
    path('apm/test', apm.APM_TEST.test_page, name='test_page'),
    path('apm/report', apm.APM_REPORT.report_home_page, name='report_home_page'),
]