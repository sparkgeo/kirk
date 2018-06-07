'''
Created on May 16, 2018

@author: kjnether
'''
# api/serializers.py

from rest_framework import serializers
from .models.Job import Job
from .models.Sources import Sources
from .models.Destinations import Destinations
from .models.FieldMap import FieldMap
from .models.JobStatistics import JobStatistics
from django.contrib.auth.models import User


class SourceDataListSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Sources
        fields = ('sourceid', 'jobid', 'sourceTable', 'sourceType', 'sourceDBSchema',
                  'sourceDBName', 'sourceDBHost', 'sourceDBPort',
                  'sourceFilePath')
        read_only_fields = ('sourceid',)


class DestinationsSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Destinations
        fields = ('dest_key', 'dest_service_name', 'dest_host', 'dest_port', 'dest_type',
                  )
        # read_only_fields = ( 'sourceid',  )


class FieldmapSerializer(serializers.ModelSerializer):

    # owner = serializers.ReadOnlyField(source='owner.username') # ADD THIS LINE

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = FieldMap
        fields = ('fieldMapId', 'jobid', 'sourceColumnName', 'destColumnName', \
                  'fmeColumnType', 'whoCreated', 'whenCreated', 'whoUpdated',
                  'whoUpdated'
                  )
        read_only_fields = ('fieldMapId',)


class JobStatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = JobStatistics
        fields = ('jobStatsId', 'jobid', 'jobStatus', 'fmeServerJobId', \
                  'jobStarted', 'jobCompleted')
        read_only_fields = ('jobStatsId',)


class JobDetailedInfoSerializer(serializers.ModelSerializer):

    sources = SourceDataListSerializer(many=True, read_only=True)
    fieldmaps = FieldmapSerializer(many=True, read_only=True)

    class Meta:
        '''
        job details Metadata
        '''
        model = Job
        fields = ('jobid', 'jobStatus', 'cronStr', 'destEnvKey', 'date_created', 'date_modified', 'sources', 'fieldmaps')
        read_only_fields = ('date_created', 'date_modified')


class JobIdlistSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """
    # read_only = True
    # sources = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    sources = SourceDataListSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')  # ADD THIS LINE
    fieldmaps = FieldmapSerializer(many=True, read_only=True)
    #destkey = serializers.PrimaryKeyRelatedField(queryset=Destinations.objects.all())
    #destkey = DestinationsSerializer(many=False, read_only=False)
    destkey = serializers.SlugRelatedField(many=False, read_only=False,
                                            queryset=Destinations.objects.all(),
                                            slug_field='dest_key', 
                                            allow_null=True)
    #destkey = serializers.ReadOnlyField(source='Destinations.dest_key')

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Job
        fields = ('jobid', 'jobStatus', 'cronStr', 'destEnvKey', 'date_created',
                  'date_modified', 'sources', 'destkey', 'owner', 'fieldmaps')
        read_only_fields = ('date_created', 'date_modified')
        depth = 1
        
    def create(self, validated_data):
        print 'validated_data', validated_data
        destinationsData = validated_data.pop('destEnvKey')
        print 'destinationsData', destinationsData
        #jobs = Job.objects.get()
        #jobs.objects.update()


class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    job = serializers.PrimaryKeyRelatedField(many=True,
                                             queryset=Job.objects.all())

    class Meta:
        """Map this serializer to the default django user model."""
        model = User
        fields = ('id', 'username', 'job')

