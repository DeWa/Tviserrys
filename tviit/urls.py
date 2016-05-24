from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='tviit_index'),
    url(r'create/$', views.create_tviit, name="create_tviit"),
    url(r'reply/$', views.reply_tviit, name="reply_tviit"),
]
