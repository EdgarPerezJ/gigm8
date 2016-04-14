"""gigm8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from gigm8app import views
from gigm8app import eventful_api

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^events/', views.events),
    url(r'^history/(?P<artist_name>\w{0,50})/$', views.history),
    url(r'^lastevents/(?P<armbid>[A-Za-z0-9\-]+)/$', views.last_events),
    url(r'^location/(?P<page>\d+)/', views.EventsbyLocation),
    url(r'^Details/', views.details),
    url(r'^getdetails/(?P<id>[\w{}.@-]{1,40})/$', views.EventDetails),
    url(r'^events_geolocation/(?P<latitude>\-?\d*\.?\d+)/(?P<longitude>\-?\d*\.?\d+)/(?P<page>\d+)', views.events_by_geolocation),
    url(r'^artist_name/(?P<page>\d+)/', views.artist_by_name),
    url(r'^admin/', include(admin.site.urls)),
]