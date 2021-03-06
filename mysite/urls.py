"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# -*- coding:utf-8 -*-

from django.conf.urls import handler404
from django.conf.urls import handler500

from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views import static
from django.conf import settings
from django.conf.urls import url
from testsite.views import error

handler404 = error.CommonError.error_404_page
handler500 = error.CommonError.error_500_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('testsite.urls',namespace='elver')),
    path('', include('social_django.urls', namespace='social')),
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),

]