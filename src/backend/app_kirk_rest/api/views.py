# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework import permissions

from .models.Destinations import Destinations
from .models.FieldMap import FieldMap
from .models.ReplicationJobs import ReplicationJobs
from .models.Sources import Sources
from .models.JobStatistics import JobStatistics
from .permissions import IsOwner
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

#     def perform_update(self, serializer):
#         print 'update: serializer', serializer
#         serializer.save(owner=self.request.user)


class SourceDataView(generics.ListCreateAPIView):
    queryset = Sources.objects.all()
    serializer_class = SourceDataListSerializer
    permission_classes = (permissions.IsAuthenticated,)

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


class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
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

