# -*- coding:utf-8 -*-
from django.urls import path
from testsite import views
# import mysite
#
# from django.conf.urls import url
# from django.views import static
# from django.conf import settings
# from django.conf.urls import handler400, handler403, handler404, handler500

app_name = 'testsite'


urlpatterns = [
    # path('report/', views.report, name='report'),
    path('login/', views.login_page, name='login_page'),
    path('login_api/', views.login_api, name='login_api'),
    path('scan_login_api', views.scan_login_api, name='scan_login_api'),
    path('scan_login/', views.scan_login, name='scan_login'),
    path('getCPUInfo/', views.getCPUInfo, name='getCPUInfo'),
    path('404/', views.page_404, name='page_404'),
    path('jira/', views.jira, name='jira'),
    path('get_apk_url/', views.get_apk_url, name='get_apk_url'),
    path('ding_build_apk/', views.ding_build_apk, name='ding_build_apk'),
    path('get_ding_key/', views.get_ding_key, name='get_ding_key'),
    path('add_log_api/', views.add_log_api, name='add_log_api'),


    path('tool/', views.tool, name='tool'),
    path('bug_monitor/', views.bug_monitor, name='bug_monitor'),

    path('apk/', views.apk, name='apk_list'),

    path('ad_sample/', views.ad_sample, name='ad_sample'),
    path('ad_sample_report/', views.ad_sample_report, name='ad_sample_report'),

    path('query_config/', views.query_config, name='query_config'),
    path('query_config_api/', views.query_config_api, name='query_config_api'),


    path('dashboard/', views.dashboard, name='dashboard'),

    path('apm_online/', views.apm_online, name='apm_online'),
    path('apm_offline/', views.apm_offline, name='apm_offline'),
    path('apm_detail/<logname>', views.apm_detail, name='apm_detail'),
    path('TItest/', views.TItest, name='TItest'),
    path('apm_api/', views.apm_api, name='apm_api'),
    path('apm_detail_api/', views.apm_detail_api, name='apm_detail_api'),
    path('get_timecost_info/', views.get_timecost_info, name='get_timecost_info'),
    path('update_timecost/', views.update_timecost, name='update_timecost'),
    path('insert_timecost/', views.insert_timecost, name='insert_timecost'),

    path('offline_log_search/', views.offline_log_search, name='offline_log_search'),
    path('offline_log/', views.offline_log, name='offline_log'),
    path('get_bi_actions/', views.get_bi_actions, name='get_bi_actions'),
    path('save_bi_actions/', views.save_bi_actions, name='save_bi_actions'),
    path('check_actions/', views.check_actions, name='check_actions'),


    path('api_test/', views.api_test, name='api_test'),
    path('apipost/', views.apipost, name='apipost'),
    path('getpost/', views.getpost, name='getpost'),
    path('getapi/', views.getapi, name='getapi'),
    path('insert_api/', views.insert_api, name='insert_api'),
    path('insert_task/', views.insert_task, name='insert_task'),
    path('update_task/', views.update_task, name='update_task'),
    path('run_task/', views.run_task, name='run_task'),
    path('get_task/', views.get_task, name='get_task'),
    path('update_case/', views.update_case, name='update_case'),


    path('test_result/', views.test_result, name='test_result'),
    path('test_result_api/', views.test_result_api, name='test_result_api'),
    path('report/<taskname>', views.report, name='report'),
    path('test_report/<id>', views.test_report, name='test_report'),

    path('api_monitor/', views.api_monitor, name='api_monitor'),
    path('api_monitor_api/', views.api_monitor_api, name='api_monitor_api'),

    path('applog/', views.applog, name='applog'),
    path('applog_detail/<logname>', views.applog_detail, name='applog_detail'),
    path('applog_api/', views.applog_api, name='applog_api'),
    path('applog_search_api/', views.applog_search_api, name='applog_search_api'),

    path('ci_server/', views.ci_server, name='ci_server'),
    path('ci_server_api/', views.ci_server_api, name='ci_server_api'),


    path('logout/', views.logout, name='logout'),
    path('detail/<apk_name>', views.detail, name='detail'),
    path('get_size/', views.get_size, name='get_size'),
    path('delete_data/', views.delete_data, name='delete_data'),
    path('', views.dashboard),
    path('change_password/', views.change_password_page, name='change_password'),
    path('change_password_api/', views.change_password_api, name='change_password_api'),
    path('task_add/', views.task_add, name='task_add'),
    path('task_del/', views.task_del, name='task_del'),

    path('galo_test/', views.galo_test, name='galo_test'),
    path('make_phone/', views.make_phone, name='make_phone'),

    path('log/', views.Log_page, name='log'),
    path('log_api/', views.Log_api, name='log_api'),

    path('bug_monitor_api/', views.bug_monitor_api, name='bug_monitor_api'),
    path('MasterList/', views.MasterList, name='MasterList'),

    path('app_debug/', views.app_debug, name='app_debug'),
    path('login_test/', views.login_test, name='login_test'),

    path('online_log_search/', views.online_log_search, name='online_log_search'),
    path('online_log/', views.online_log_page, name='online_log'),
    # url(r'^static/(?P<path>.*)$', static.serve,
    #     {'document_root': settings.STATIC_ROOT}, name='static')
    path('app_debug_page/', views.app_debug_page, name='app_debug_page'),
    path('app_debug_api/', views.app_debug_api, name='app_debug_api'),
    path('app_debug_add_anm/', views.app_debug_add_anm, name='app_debug_add_anm'),
]

# handler400 = views.page_404