'''
Created on May 16, 2018

@author: kjnether
'''
from __future__ import unicode_literals

from django.conf.urls import url
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view

from .views import AddUserView
from .views import CreateJobView
from .views import DestinationsDetailsView
from .views import DestinationsView
from .views import FieldMapDetailsView
from .views import FieldMapView
from .views import JobDestinationView
from .views import JobDetailsView
from .views import JobFieldMapsView
from .views import JobSourcesView
from .views import JobStatisticsDetailsView
from .views import JobStatisticsView
from .views import SourceDataView
from .views import SourcesDetailsView
from .views import UserDetailsView
from .views import TransformersView
from .views import TransformerDetailsView
from .views import JobTransformersView
from .views import JobTransformerView



schema_view = get_swagger_view(title='KIRK')

urlpatterns = {

    url(r'^$', schema_view),
    url(r'^api/v1/jobs/$', CreateJobView.as_view(), name="job_create"),
    # url(r'^job/$', JobCompleteView.as_view(), name="create"),
    url(r'^api/v1/jobs/(?P<jobid>[0-9]+)/$',
        JobDetailsView.as_view(), name="job_details"),
    url(r'^api/v1/jobs/(?P<jobid>[0-9]+)/sources/$', JobSourcesView.as_view(),
        name='job_sources'),
    url(r'^api/v1/jobs/(?P<jobid>[0-9]+)/transformers/$', JobTransformersView.as_view(),
        name='job_transformers'),
    url(r'^api/v1/jobs/(?P<jobid>[0-9]+)/transformers/(?P<transformer_id>[0-9]+)/$', JobTransformerView.as_view(),
        name='job_transformer'),
    url(r'^api/v1/jobs/(?P<jobid>[0-9]+)/destination/$', JobDestinationView.as_view(),
        name='job_destination'),
    url(r'^api/v1/jobs/(?P<jobid>[0-9]+)/fieldmaps/$', JobFieldMapsView.as_view(), name='job_fieldmaps'),
    url(r'^api/v1/sources/$', SourceDataView.as_view(), name='source_create'),
    url(r'^api/v1/sources/(?P<sourceid>[0-9]+)/$',
        SourcesDetailsView.as_view(), name="source_details"),
    url(r'^api/v1/destinations/$', DestinationsView.as_view(), name='destination_create'),
    url(r'^api/v1/destinations/(?P<dest_key>[a-zA-Z]+)/$',
        DestinationsDetailsView.as_view(), name="destinations_details"),
    url(r'^api/v1/fieldmaps/$', FieldMapView.as_view(), name='fieldmap_create'),
    url(r'^api/v1/fieldmaps/(?P<fieldMapId>[0-9]+)/$',
        FieldMapDetailsView.as_view(), name="fieldmap_details"),
    url(r'^api/v1/jobstats/$', JobStatisticsView.as_view(), name='jobstats_create'),
    url(r'^api/v1/jobstats/(?P<jobStatsId>[0-9]+)/$',
        JobStatisticsDetailsView.as_view(), name="jobstats_details"),
    url(r'^api/v1/transformers/$', TransformersView.as_view(), name='transformers_create'), # working
    url(r'^api/v1/transformers/(?P<transformer_id>[0-9]+)/$',
        TransformerDetailsView.as_view(), name="transformers_details"), 
    url(r'^api/v1/users/$', AddUserView.as_view(), name="users"),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/$',
        UserDetailsView.as_view(), name="user_details"),
    # url(r'^get_auth_token/$', obtain_auth_token, name='get_auth_token'),

    url(r'^api/v1/auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
    #url(r'^api/v1/get-token/', obtain_auth_token),

}

urlpatterns = format_suffix_patterns(urlpatterns)
