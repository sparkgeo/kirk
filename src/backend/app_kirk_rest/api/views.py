# -*- coding: utf-8 -*-
from __future__ import unicode_literals





from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import JobIdlistSerializer
from .serializers import SourceDataListSerializer
from .models.Job import Job
from .models.Sources import Sources

class CreateJobView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Job.objects.all()
    serializer_class = JobIdlistSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
        
class JobDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    lookup_field  = 'jobid'
    queryset = Job.objects.all()
    serializer_class = JobIdlistSerializer
    
class SourceDataView(generics.ListCreateAPIView):
    queryset = Sources.objects.all()
    serializer_class = SourceDataListSerializer
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
    
# class JobCompleteView(generics.ListCreateAPIView):
#     queryset = Job.objects.all()

    
    