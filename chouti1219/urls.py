"""chouti1219 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from chouti01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^register/', views.register),
    url(r'^getmbcode/', views.getmbcode),
    url(r'^logout/', views.logout),
    url(r'^urlpublish/', views.urlpublish),
    url(r'^favor/', views.favor),
    url(r'^content/', views.content),
    url(r'^searchtable/', views.searchtable),
    url(r'^abctest/', views.abctest),
]
