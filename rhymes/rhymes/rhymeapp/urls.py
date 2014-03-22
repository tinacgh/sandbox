from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(r'^$', views.home),
                       url(r'^build/$', views.populatedb),
                       url(r'^match/(?P<input>\S+)$', views.match),
                       url(r'^search/$', views.search),
                       )
