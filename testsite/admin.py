from django.contrib import admin
from testsite import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Log)
admin.site.register(models.AutomationTask)
admin.site.register(models.StressTestTask)


