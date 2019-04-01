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
from django.contrib import admin
from django.http import HttpResponseServerError
from django.urls import include, path

from MedusaII import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('l/',include('leituras.urls')),
    path('vc/', include('voting.urls')),
    path('accounts/', include('escola.urlsAuth')),
    # path('escola/', include('escola.urls')),
    path('', include('escola.urls')),
    path('', include('django_prometheus.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
if settings.DEBUG:
    urlpatterns.append(path('500', lambda request: HttpResponseServerError()))