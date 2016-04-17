from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout),
    url(r'^password_change/$', auth_views.password_change),
    url(r'^password_change/done/$', auth_views.password_change_done),
    url(r'^password_reset/$', auth_views.password_reset),
    url(r'^password_reset/done/$', auth_views.password_reset_done),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm),
    url(r'^reset/done/$', auth_views.password_reset_complete),
]
