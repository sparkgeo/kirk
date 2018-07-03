# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework import permissions

#from .models.User import User
from .models.Destinations import Destinations
from .models.FieldMap import FieldMap
from .models.ReplicationJobs import ReplicationJobs
from .models.Sources import Sources
from .models.JobStatistics import JobStatistics
#from .permissions import IsOwner
from .serializers import DestinationsSerializer
from .serializers import FieldmapSerializer
from .serializers import JobIdlistSerializer
from .serializers import JobStatisticsSerializer
from .serializers import SourceDataListSerializer
from .serializers import UserSerializer



# Create your views here.
class CreateJobView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = ReplicationJobs.objects.all()
    serializer_class = JobIdlistSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # if we wanted only owners of the job to be able to modify then use this
    # permission class.
    # permission_classes = (
    #    permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new job item."""
        print 'create: serializer', serializer
        serializer.save(owner=self.request.user)


class JobDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    lookup_field = 'jobid'
    queryset = ReplicationJobs.objects.all()
    serializer_class = JobIdlistSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_update(self, serializer):
        print 'update: serializer', serializer
        serializer.save(owner=self.request.user)



class SourceDataView(generics.ListCreateAPIView):
    queryset = Sources.objects.all()
    serializer_class = SourceDataListSerializer
    #permission_classes = (permissions.IsAuthenticated,)

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
    #queryset = Sources.objects.all()
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

class JobDestinationView(generics.ListCreateAPIView):
    serializer_class = DestinationsSerializer
    
    def get_queryset(self):
        print 'kwargs: ', self.kwargs
        jobid = self.kwargs['jobid']
        print 'jobid: {0}'.format(jobid)
        dest = ReplicationJobs.objects.filter(jobid=jobid)
        destKey =  dest[0].destEnvKey
        # now get the full destination object
        destObj = Destinations.objects.filter(dest_key=destKey)
        return destObj
    
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
    queryset = FieldMap.objects.all()
    serializer_class = FieldmapSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # lookup_field  = 'sourceid'

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


class FieldMapDetailsView(generics.ListCreateAPIView):
    queryset = FieldMap.objects.all()
    serializer_class = FieldmapSerializer
    permission_classes = (permissions.IsAuthenticated,)


class JobStatisticsView(generics.ListCreateAPIView):
    queryset = JobStatistics.objects.all()
    serializer_class = JobStatisticsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


class JobStatisticsDetailsView(generics.ListAPIView):
    '''
    handles GET, PUT, and DELETE requests for sources
    '''
    # lookup_field = 'sourceid'
    queryset = JobStatistics.objects.all()
    serializer_class = JobStatisticsSerializer
    permission_classes = (permissions.IsAuthenticated,)

