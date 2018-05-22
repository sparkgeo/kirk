'''
Created on May 16, 2018

@author: kjnether
'''
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateJobView
from .views import JobDetailsView
from .views import SourceDataView
from .views import SourcesDetailsView
#from .views import JobCompleteView

urlpatterns = {
    url(r'^job/$', CreateJobView.as_view(), name="create"),
    #url(r'^job/$', JobCompleteView.as_view(), name="create"),
    url(r'^job/(?P<jobid>[0-9]+)/$',
        JobDetailsView.as_view(), name="details"),
    url(r'^sources/$', SourceDataView.as_view(), name='source_create'),
    url(r'^sources/(?P<sourceid>[0-9]+)/$',
        SourcesDetailsView.as_view(), name="source_details"),

}

urlpatterns = format_suffix_patterns(urlpatterns)
