"""FreeBees URL Configuration

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
from django.conf.urls import url
from django.urls import path, include
from GiveFree.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', LandingPageView.as_view()),
    url(r'^main$', MainPageView.as_view()),
    url(r'^admins$', AdminsList.as_view(), name='admins'),
    url(r'^add/admin$', AddAdmin.as_view()),
    url(r'^edit/admin/(?P<pk>\d+)$', EditAdminView.as_view()),
    url(r'^delete/admin/(?P<pk>\d+)$', DeleteAdminView.as_view()),
    url(r'^add/institution$', AddInstitutionView.as_view()),
    url(r'^institutions$', InstitutionListView.as_view(), name='institutions'),
    url(r'^delete/institution/(?P<pk>\d+)$', DeleteInstitutionView.as_view()),
    url(r'^edit/institution/(?P<id>\d+)$', EditInstitutionView.as_view()),
]
