from django.contrib import admin
from testsite import models
# Register your models here.
admin.site.register(models.Apk)
admin.site.register(models.Size)
admin.site.register(models.User)
admin.site.register(models.Ad_sample_info)
admin.site.register(models.Ad_sample_stat)
admin.site.register(models.Server_applog)
admin.site.register(models.APIinfo)
admin.site.register(models.APItask)
admin.site.register(models.Taskresult)
admin.site.register(models.operation_log)