from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^tviit/$', views.TviitList.as_view()),
    url(r'^tviit/(?P<uuid>[^/]+)/$', views.TviitDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)