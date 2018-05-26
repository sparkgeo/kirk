# -*- coding: utf-8 -*-
from __future__ import unicode_literals





from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .permissions import IsOwner
from .serializers import JobIdlistSerializer
from .serializers import SourceDataListSerializer
from .serializers import DestinationsSerializer
from .serializers import UserSerializer
from .models.Job import Job
from .models.Sources import Sources
from .models.Destinations import Destinations
from rest_framework import permissions
from django.contrib.auth.models import User


class CreateJobView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Job.objects.all()
    serializer_class = JobIdlistSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # if we wanted only owners of the job to be able to modify then use this 
    # permission class.
    #permission_classes = (
    #    permissions.IsAuthenticated, IsOwner)
    
    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save(owner=self.request.user)
        
class JobDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    lookup_field  = 'jobid'
    queryset = Job.objects.all()
    serializer_class = JobIdlistSerializer
    permission_classes = (permissions.IsAuthenticated,)

    
class SourceDataView(generics.ListCreateAPIView):
    queryset = Sources.objects.all()
    serializer_class = SourceDataListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    #lookup_field  = 'sourceid'

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
        
class SourcesDetailsView(generics.RetrieveUpdateDestroyAPIView):
    '''
    handles GET, PUT, and DELETE requests for sources
    '''
    lookup_field  = 'sourceid'
    queryset = Sources.objects.all()
    serializer_class = SourceDataListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
class DestinationsView(generics.ListCreateAPIView):
    lookup_field  = 'dest_key'
    queryset = Destinations.objects.all()
    serializer_class = DestinationsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
    
class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
