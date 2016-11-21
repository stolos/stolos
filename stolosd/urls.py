"""stolos_watchd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from djoser import views as djoser_views
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from dashboard import views as dashboard_views
from users.views import CustomLoginView

urlpatterns = [
    url(r'^$', dashboard_views.projects_view),
    url(r'^login/$', auth_views.login, name='web_login'),
    url(r'^logout/$', auth_views.logout_then_login, name='web_logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/a0.1/auth/login', CustomLoginView.as_view()),
    url(r'^api/a0.1/auth/logout/', djoser_views.LogoutView.as_view(), name='logout'),
    url(r'^api/a0.1/auth/password/', djoser_views.SetPasswordView.as_view()),
    url(r'^', include('projects.urls')),
    url(r'^', include('users.urls')),
]
