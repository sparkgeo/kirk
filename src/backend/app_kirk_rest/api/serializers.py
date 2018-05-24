'''
Created on May 16, 2018

@author: kjnether
'''
# api/serializers.py

from rest_framework import serializers
from .models.Job import Job
from .models.Sources import Sources



class SourceDataListSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Sources
        fields = ('sourceid', 'jobid', 'sourceTable', 'sourceType', 'sourceDBSchema',
                  'sourceDBName', 'sourceDBHost', 'sourceDBPort',
                  'sourceFilePath')
        read_only_fields = ( 'sourceid',  )


class JobDetailedInfoSerializer(serializers.ModelSerializer):
    
    sources = SourceDataListSerializer(many = True, read_only=True)
    
    class Meta:
        '''
        job details Metadata
        '''
        model = Job
        fields = ('jobid', 'jobStatus','cronStr', 'date_created', 'date_modified', 'sources')

class JobIdlistSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """
    # read_only = True
    #sources = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    sources = SourceDataListSerializer(many = True, read_only=True)
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Job
        fields = ('jobid', 'jobStatus', 'date_created', 'date_modified', 'sources')
        read_only_fields = ('date_created', 'date_modified')

# class JobCompleteSerializer(serializers.ModelSerializer):
#     '''
#     Builds the relationships necessary to display all the related job
#     information.
#     '''
#     sources = serializers.PrimaryKeyRelatedField(many=True, read_only=False)
# 
#     class Meta:
#         model = Job
#         fields = ('jobid', 'jobStatus', 'date_created', 'date_modified', 'sources')

