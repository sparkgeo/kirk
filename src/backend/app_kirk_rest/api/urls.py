'''
Created on May 16, 2018

@author: kjnether
'''
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token  # add this import
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CreateJobView
from .views import DestinationsView
from .views import JobDetailsView
from .views import SourceDataView
from .views import SourcesDetailsView
from .views import UserDetailsView
from .views import UserView


urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', # ADD THIS URL
                               namespace='rest_framework')),
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'users/(?P<pk>[0-9]+)/$',
        UserDetailsView.as_view(), name="user_details"),
    url(r'^get-token/', obtain_auth_token), # Add this line

    url(r'^job/$', CreateJobView.as_view(), name="job_create"),
    #url(r'^job/$', JobCompleteView.as_view(), name="create"),
    url(r'^job/(?P<jobid>[0-9]+)/$',
        JobDetailsView.as_view(), name="job_details"),
    url(r'^sources/$', SourceDataView.as_view(), name='source_create'),
    url(r'^sources/(?P<sourceid>[0-9]+)/$',
        SourcesDetailsView.as_view(), name="source_details"),
    url(r'^destinations/$', DestinationsView.as_view(), name='destination_create')
}

urlpatterns = format_suffix_patterns(urlpatterns)
