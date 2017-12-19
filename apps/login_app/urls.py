# app level

from django.conf.urls import url
from . import views
    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^add_plan$', views.add_plan),
    url(r'^create$', views.create_trip),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^info/(?P<trip_id>\d+)$', views.info),
    url(r'^untrip/(?P<trip_id>\d+)$', views.untrip)
]