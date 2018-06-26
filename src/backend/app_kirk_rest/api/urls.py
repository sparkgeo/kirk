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
from .views import FieldMapView
from .views import JobStatisticsView
from .views import JobStatisticsDetailsView
from .views import DestinationsDetailsView
from .views import FieldMapDetailsView
from . import views as local_view
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='KIRK')



urlpatterns = {
    
    url(r'^$', schema_view),

    url(r'^jobs/$', CreateJobView.as_view(), name="job_create"),
    # url(r'^job/$', JobCompleteView.as_view(), name="create"),
    url(r'^jobs/(?P<jobid>[0-9]+)/$',
        JobDetailsView.as_view(), name="job_details"),
    url(r'^sources/$', SourceDataView.as_view(), name='source_create'),
    url(r'^sources/(?P<sourceid>[0-9]+)/$',
        SourcesDetailsView.as_view(), name="source_details"),
    url(r'^destinations/$', DestinationsView.as_view(), name='destination_create'),
    url(r'^destinations/(?P<dest_key>[a-zA-Z]+)/$',
        DestinationsDetailsView.as_view(), name="destinations_details"),
    url(r'^fieldmaps/$', FieldMapView.as_view(), name='fieldmap_create'),
    url(r'^fieldmaps/(?P<fieldMapId>[0-9]+)/$',
        FieldMapDetailsView.as_view(), name="fieldmap_details"),
    url(r'^jobstats/$', JobStatisticsView.as_view(), name='jobstats_create'),
    url(r'^jobstats/(?P<jobStatsId>[0-9]+)/$',
        JobStatisticsDetailsView.as_view(), name="jobstats_details"),
    #url(r'^login/$', local_views.get_auth_token, name='login'),

    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'users/(?P<pk>[0-9]+)/$',
        UserDetailsView.as_view(), name="user_details"),
    #url(r'^get_auth_token/$', obtain_auth_token, name='get_auth_token'),    

    
    #url(r'^get-token/', obtain_auth_token),  # Add this line
    url(r'^auth/', include('rest_framework.urls',  # ADD THIS URL
                               namespace='rest_framework')),

}

urlpatterns = format_suffix_patterns(urlpatterns)
