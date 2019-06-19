"""MedusaII URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
#  Developed by Vinicius José Fritzen
#  Last Modified 20/04/19 08:49.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.views.defaults import server_error, page_not_found
from django.contrib import admin
from django.http import HttpResponseServerError
from django.urls import include, path

from MedusaII import settings

urlpatterns = \
    [
        path('admin/', admin.site.urls),
        path('accounts/', include('escola.urlsAuth')),
        # path('escola/', include('escola.urls')),
        path('', include('escola.urls')),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        path('', include('pwa.urls')),
    ]
if settings.DEBUG:
    urlpatterns.append(path('500', server_error))
    urlpatterns.append(path('404', page_not_found))


handler500 = 'escola.views.handler500'
