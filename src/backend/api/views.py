# -*- coding: utf-8 -*-
'''
views used for kirk

'''
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions

from .models.Destinations import Destinations
from .models.FieldMap import FieldMap
from .models.JobStatistics import JobStatistics
from .models.ReplicationJobs import ReplicationJobs
from .models.Sources import Sources
from .models.Transformers import Transformers

from .serializers import DestinationsSerializer
from .serializers import FieldmapDataTypeSerializer
from .serializers import FieldmapSerializer
from .serializers import JobIdlistSerializer
from .serializers import JobStatisticsSerializer
from .serializers import SourceDataListSerializer
from .serializers import UserSerializer
from .serializers import TransformerSerializer


# Create your views here.
class CreateJobView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = ReplicationJobs.objects.all()  # pylint: disable=no-member
    serializer_class = JobIdlistSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # if we wanted only owners of the job to be able to modify then use this
    # permission class.
    # permission_classes = (
    #    permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new job item."""
        # print 'create: serializer', serializer
        serializer.save(owner=self.request.user)


class JobDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    lookup_field = 'jobid'
    #queryset = ReplicationJobs.objects.all()
    serializer_class = JobIdlistSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_update(self, serializer):
        print(f'update: serializer {serializer}')
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        jobid = self.kwargs['jobid']
        #print(f'jobid: {jobid}') 
        qs = ReplicationJobs.objects.filter(jobid=jobid)
        return qs


class SourceDataView(generics.ListCreateAPIView):
    queryset = Sources.objects.all()
    serializer_class = SourceDataListSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    # lookup_field  = 'sourceid'

    def perform_create(self, serializer):
        """Save the post data when creating a new source dataset."""
        serializer.save()


class SourcesDetailsView(generics.RetrieveUpdateDestroyAPIView):
    '''
    handles GET, PUT, and DELETE requests for sources
    '''
    lookup_field = 'sourceid'
    queryset = Sources.objects.all()
    serializer_class = SourceDataListSerializer
    permission_classes = (permissions.IsAuthenticated,)


class JobSourcesView(generics.ListCreateAPIView):
    # queryset = Sources.objects.all()
    serializer_class = SourceDataListSerializer

    def get_queryset(self):
        jobid = self.kwargs['jobid']
        sources = Sources.objects.filter(jobid=jobid)
        return sources


class DestinationsView(generics.ListCreateAPIView):
    lookup_field = 'dest_key'
    queryset = Destinations.objects.all()
    serializer_class = DestinationsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


class DestinationsDetailsView(generics.ListCreateAPIView):
    lookup_field = 'dest_key'
    queryset = Destinations.objects.all()
    serializer_class = DestinationsSerializer
    permission_classes = (permissions.IsAuthenticated,)


class JobDestinationView(generics.RetrieveAPIView):
    serializer_class = DestinationsSerializer

    def get_object(self):
        # print 'kwargs: ', self.kwargs
        jobid = self.kwargs['jobid']
        # print 'jobid: {0}'.format(jobid)
        dest = ReplicationJobs.objects.filter(jobid=jobid)
        destKey = dest[0].destEnvKey
        # now get the full destination object
        destObj = Destinations.objects.filter(dest_key=destKey)
        # print 'destObj: {0}'.format(destObj)
        return destObj[0]


class AddUserView(generics.ListCreateAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new source dataset."""
        serializer.save()


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FieldMapView(generics.ListCreateAPIView):
    '''
    View to create and list fieldmaps
    '''
    queryset = FieldMap.objects.all()
    serializer_class = FieldmapSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        # serializer.save()
        serializer.save(whoCreated=self.request.user, 
                        whoUpdated=self.request.user)


class TransformersView(generics.ListCreateAPIView):
    '''
    View to create and list Transformers
    '''
    queryset = Transformers.objects.all()  # @UndefinedVariable
    serializer_class = TransformerSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save(whoCreated=self.request.user, 
                        whoUpdated=self.request.user)


class TransformerDetailsView(generics.RetrieveUpdateDestroyAPIView):
    '''
    view used to provide details for individual field map records.
    '''
    queryset = Transformers.objects.all()  # @UndefinedVariable
    lookupfield = 'transformer_id'
    serializer_class = TransformerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        transformer_id = self.kwargs['transformer_id']
        trans_map = Transformers.objects.filter(transformer_id=transformer_id)  # @UndefinedVariable
        obj = trans_map.get(pk=transformer_id)
        return obj


class FieldMapDetailsView(generics.RetrieveUpdateDestroyAPIView):
    '''
    view used to provide details for individual field map records.
    '''
    queryset = FieldMap.objects.all()
    lookupfield = 'fieldMapId'
    serializer_class = FieldmapDataTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        fldmapid = self.kwargs['fieldMapId']
        fldmap = FieldMap.objects.filter(fieldMapId=fldmapid)
        obj = fldmap.get(pk=fldmapid)
        return obj


class JobFieldMapsView(generics.ListCreateAPIView):
    '''view used to provide fieldmaps for a specific job'''
    # queryset = Sources.objects.all()
    serializer_class = FieldmapDataTypeSerializer

    def get_queryset(self):
        jobid = self.kwargs['jobid']
        fldMaps = FieldMap.objects.filter(jobid=jobid)
        return fldMaps


class JobTransformersView(generics.ListCreateAPIView):
    serializer_class = TransformerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        jobid = self.kwargs['jobid']
        transformer = Transformers.objects.filter(jobid=jobid)
        return transformer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save(whoCreated=self.request.user, whoUpdated=self.request.user)


class JobTransformerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transformers.objects.all()
    lookupfield = 'transformer_id'
    serializer_class = TransformerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        transformer_id = self.kwargs['transformer_id']
        jobid = self.kwargs['jobid']
        # self.kwargs {u'transformer_id': u'1', u'jobid': u'2'}
        transformers = Transformers.objects.filter(transformer_id=transformer_id, jobid=jobid)
        obj = transformers.get(pk=transformer_id)
        return obj


class JobStatisticsView(generics.ListCreateAPIView):
    '''
    view used to create new statistics line, and get complete list of stats.
    '''
    queryset = JobStatistics.objects.all()
    serializer_class = JobStatisticsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()

    # queryset = Sources.objects.all()
    serializer_class = SourceDataListSerializer

    def get_queryset(self):
        jobid = self.kwargs['jobid']
        sources = Sources.objects.filter(jobid=jobid)
        return sources


class JobStatisticsDetailsView(generics.ListAPIView):
    '''
    handles GET, PUT, and DELETE requests for sources
    '''
    # lookup_field = 'sourceid'
    queryset = JobStatistics.objects.all()
    serializer_class = JobStatisticsSerializer
    permission_classes = (permissions.IsAuthenticated,)
