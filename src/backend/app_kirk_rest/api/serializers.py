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


class JobDetailedInfoSerializer(serializers.PrimaryKeyRelatedField):

    sources = SourceDataListSerializer(many=True, read_only=True)
    fieldmaps = FieldmapSerializer(many=True, read_only=True)

    class Meta:
        '''
        job details Metadata
        '''
        model = Job
        fields = ('jobid', 'jobStatus', 'cronStr', 'destEnvKey', 'date_created', 'date_modified', 'sources', 'fieldmaps')
        read_only_fields = ('date_created', 'date_modified')

class JobDestSerializer(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        print 'context:', self.context['request'].data
        filteredDests = None
        queryset = self.queryset
        if 'destkey' in self.context['request'].data:
            # if the destkey relates to Destinations then keep, otherwise set to None
            ProvidedEnvKey = self.context['request'].data['destkey']
            print 'ProvidedEnvKey', ProvidedEnvKey
            
            filteredDests = Destinations.objects.filter(dest_key=ProvidedEnvKey)
            print 'filteredDests', filteredDests
        if filteredDests:
            #destKey = ProvidedEnvKey
            queryset = queryset.filter(dest_key=ProvidedEnvKey)
        else:
            #destKey = None
            queryset = queryset.filter()
        #print 'return data:', destKey
        print 'queryset', queryset
        return queryset

class JobIdlistSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """
    # read_only = True
    # sources = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    sources = SourceDataListSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')  # ADD THIS LINE
    fieldmaps = FieldmapSerializer(many=True, read_only=True)
        
#     destkey = serializers.SlugRelatedField(read_only=True,
#                                             slug_field='dest_key', 
#                                             allow_null=True)
#                                             #queryset=Destinations.objects.all())
    
    destkey = JobDestSerializer( queryset=Destinations.objects.all(),
                                source='Destinations', 
                                required=False)
                                #slug_field='dest_key',
    #destkey = serializers.PrimaryKeyRelatedField(read_only=False)
    #dests = serializers.PrimaryKeyRelatedField(queryset=Destinations.objects.filter())
    #destkey = DestinationsSerializer(many=True, read_only=False)
    #destkey = serializers.RelatedField(read_only=True)
    #destEnvKey = serializers.CharField(source='Destinations.dest_key', allow_blank=True, allow_null=True, required=False)


#     dests = Destinations.objects.all()
#     print 'dests:', dests
#     for dest in dests:
#         print 'dest', dest
    
    #destkey = serializers.PrimaryKeyRelatedField(queryset=Destinations.objects.all(), pk_field='dest_key')
    #destkey = serializers.ReadOnlyField(source='Destinations.dest_key')

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Job
        fields = ('jobid', 'jobStatus', 'cronStr', 'destEnvKey', 'date_created',
                  'date_modified', 'sources', 'owner', 'fieldmaps', 'destkey')
        read_only_fields = ('date_created', 'date_modified')
        depth = 1
        
    def create(self, validated_data):
        # validated_data {'owner': <User: spock>, u'cronStr': u'some', 
        #                 u'jobStatus': u'TESTING5', 
        #                 u'Destinations': <Destinations: DLV>}
        #
        print 'here'
        print 'validated_data', validated_data
        # {'owner': <User: spock>, u'dests': <Destinations: DLV>, u'cronStr': u'some', u'jobStatus': u'TESTING5'}
        destKey = validated_data['Destinations']
        print 'destkey value:', destKey
        del validated_data['Destinations']
        validated_data['destEnvKey'] = destKey
        print 'validated_data after fix:', validated_data
        retval = Job.objects.create(**validated_data)
        retval.save()
        print 'returned from attempted create: ', retval, type(retval)
        return retval
    
    def update(self, instance, validated_data):
        print 'update: instance', instance
        print 'update: validated_data', validated_data
        #status = validated_data.pop('status')
        #instance.status_id = status.id
        # ... plus any other fields you may want to update
        return instance



class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    job = serializers.PrimaryKeyRelatedField(many=True,
                                             queryset=Job.objects.all())

    class Meta:
        """Map this serializer to the default django user model."""
        model = User
        fields = ('id', 'username', 'job')

