from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.ViewView.as_view(), name='profile_own_view'),
    url(r'^edit/', views.EditView.as_view(), name='profile_edit'),
    url(r'^view/', views.ViewView.as_view(), name='profile_own_view'),
    url(r'^view/(?P<username>[a-zA-Z0-9_-]+)/$', views.ViewView.as_view(), name='profile_view'),
    url(r'^delete/$', views.delete_account, name="delete_account"),
]
