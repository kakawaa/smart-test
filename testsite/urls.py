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
from testsite.views import code
from testsite.views import app



app_name = 'testsite'
urlpatterns = [
    path('',login.Login.login_page, name='login_page'),

    ######【Login】
    path('login/signin', login.Login.login_page, name='login_page'),
    path('login/signup', login.Login.sign_up_page, name='sign_up_page '),
    path('sign_up_api/', login.Login.sign_up_api, name='sign_up_api '),
    path('logout/', login.Login.logout, name='logout'),
    path('login_api/', login.Login.login_api, name='login_api '),

    path('scan_login/', login.Login.scan_login, name='scan_login '),
    path('scan_login_api/', login.Login.scan_login_api, name='scan_login_api '),

    ######【Setting】
    path('setting/profile', user.Setting.setting_page, name='setting_page'),

    ######【Activity】
    path('activity/', user.UserActivity.user_activity_page, name='user_activity_page'),

    ######【BUILDER】
    path('builder/<home_path>', builder.Builder.builder_page, name='builder_page'),
    path('builder/job/<jobname>', builder.Builder.builder_detail_page, name='builder_detail_page'),
    path('builder/job/<jobname>/<item>', builder.Builder.builder_step_page, name='builder_step_page'),

    ######【APK - 信息列表】
    path('apk/info', apk.INFO.apk_info_page, name='apk_info_page'),
    path('get_apk_info_api/', apk.INFO.get_apk_info_api, name='get_apk_info_api'),
    ######【APK - 漏洞扫描】
    path('apk/virus_scan', apk.VIRUS_SCAN.virus_scan_page, name='virus_scan_page'),
    ######【APK - 加固】
    path('apk/reinforce', apk.REINFORCE.reinforce_page, name='reinforce_page'),

    ######【API TEST - 手工测试】
    path('api_test/post', api.API_POST.post_page, name='post_page'),
    path('api_test/demo', api.API_POST.demo_api, name='demo_api'),
    path('api_test/get_response', api.API_POST.get_response_api, name='get_response_api'),
    ######【API TEST - 自动化测试】
    path('api_test/automation', api.API_TASK.task_page, name='task_page'),
    path('api_test/automation/<taskname>', api.API_TASK.task_content_page, name='task_content_page'),
    path('api_test/automation/<taskname>/report/<run_id>', api.API_TASK.task_report_page, name='task_report_page'),
    path('api_test/automation/<taskname>/config', api.API_TASK.task_more_page, name='task_more_page'),
    path('api_test/automation/<taskname>/<apiname>/result/<run_id>', api.API_TASK.task_result_page, name='task_result_page'),
    path('api_test/automation/<taskname>/<apiname>', api.API_TASK.api_case_page, name='api_case_page'),
    path('api_test/automation/<taskname>/<apiname>/<casename>', api.API_TASK.api_case_page, name='api_case_page'),

    path('api_test/api/create_task', api.API_TASK.create_task_api, name='create_task_api'),
    path('api_test/api/edit_task', api.API_TASK.edit_task_api, name='edit_task_api'),
    path('api_test/api/get_task', api.API_TASK.get_task_api, name='get_task_api'),
    path('api_test/api/run_task', api.API_TASK.run_task_api, name='run_task_api'),
    path('api_test/api/delete_task', api.API_TASK.delete_task_api, name='delete_task_api'),
    path('api_test/api/create_task_content', api.API_TASK.create_task_content_api, name='create_task_content_api'),
    path('api_test/api/edit_task_content', api.API_TASK.edit_task_content_api, name='edit_task_content_api'),
    path('api_test/api/set_apiname_status', api.API_TASK.set_apiname_status_api, name='set_apiname_status_api'),
    path('api_test/api/get_online_apiname', api.API_TASK.get_online_apiname_api,name='get_online_apiname_api'),
    path('api_test/api/run_jenkins_job', api.API_TASK.run_jenkins_job_api, name='run_jenkins_job_api'),
    path('api_test/api/run_task_content', api.API_TASK.run_task_content_api, name='run_task_content_api'),
    path('api_test/api/delete_task_content', api.API_TASK.delete_task_content_api, name='delete_task_content_api'),
    path('api_test/api/create_task_case', api.API_TASK.create_task_case_api, name='create_task_case_api'),
    path('api_test/api/edit_task_case', api.API_TASK.edit_task_case_api, name='edit_task_case_api'),
    path('api_test/api/edit_case_assert', api.API_TASK.edit_case_assert_api, name='edit_case_assert_api'),
    path('api_test/api/delete_task_case', api.API_TASK.delete_task_case_api, name='delete_task_case_api'),
    path('api_test/api/get_newcase', api.API_TASK.get_newcase_api, name='get_newcase_api'),
    path('api_test/api/create_case_assert', api.API_TASK.create_case_assert_api, name='create_case_assert_api'),
    path('api_test/api/delete_case_assert', api.API_TASK.delete_case_assert_api, name='delete_case_assert_api'),
    path('api_test/api/debug_case_assert', api.API_TASK.debug_case_assert_api, name='debug_case_assert_api'),
    path('api_test/api/debug_case_script', api.API_TASK.debug_case_script_api, name='debug_case_script_api'),
    path('api_test/api/get_timer_task', api.API_TASK.get_timer_task_api, name='get_timer_task_api'),
    path('api_test/api/add_task_user', api.API_TASK.add_task_user_api, name='add_task_user_api'),
    path('api_test/api/remove_task_user', api.API_TASK.remove_task_user_api, name='remove_task_user_api'),

    ######【API TEST - 压力测试】
    path('api_test/stress', api.API_STRESS_TEST.stress_test_page, name='stress_test_page'),

    ######【SERVER - 服务监控】
    path('server/monitor', server.MONITOR.server_monitor_page, name='server_monitor_page'),
    ######【SERVER - 异常日志】
    path('server/log', server.LOG.server_log_page, name='server_log_page'),

    ######【TIMELINE】
    path('timeline/', timeline.Timeline.timeline_page, name='timeline_page'),

    ######【DOCUMENT】
    path('doc/<path>', doc.Document.document_page, name='document_page'),

    ######【APM - 性能测试】
    path('apm/test', apm.APM_TEST.test_page, name='test_page'),
    ######【APM - 云端报告】
    path('apm/report', apm.APM_REPORT.report_home_page, name='report_home_page'),
    ######【CODE - 静态代码扫描】
    path('code/analysis', code.Analysis.code_analysis_page, name='code_analysis_page'),
    ######【CODE - 代码覆盖率】
    path('code/coverage', code.Coverage.code_coverage_page, name='code_coverage_page'),

    ######【APP】
    path('app/feedback', app.FeedBack.feedback_page, name='feedback_page'),
    path('app/action', app.Action.action_log_page, name='action_log_page'),
    path('app/log', app.APP_LOG.app_log_page, name='app_log_page'),
    path('app/crash', app.Crash.crash_log_page, name='crash_log_page'),

]