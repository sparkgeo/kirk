'''
Created on May 16, 2018

@author: kjnether
'''
# api/serializers.py

from rest_framework import serializers
from .models.ReplicationJobs import ReplicationJobs
from .models.Sources import Sources
from .models.Destinations import Destinations
from .models.FieldMap import FieldMap
from .models.JobStatistics import JobStatistics
from .models.DataTypes import FMEDataTypes
# from .models.User import User
from django.contrib.auth.models import User
import sys

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

    whoCreated = serializers.ReadOnlyField(source='whoCreated.username') # ADD THIS LINE
    whoUpdated = serializers.ReadOnlyField(source='whoUpdated.username') # ADD THIS LINE
    
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = FieldMap
        fields = ('fieldMapId', 'jobid', 'sourceColumnName', 'destColumnName', \
                  'fmeColumnType', 'whoCreated', 'whenCreated', 'whoUpdated',
                  'whenUpdated'
                  )
        read_only_fields = ('fieldMapId',)


class FieldmapDataTypeSerializer(serializers.ModelSerializer):

    fmeColumnType = serializers.SlugRelatedField(read_only=False,
                                               slug_field='fieldType',
                                               queryset=FMEDataTypes.objects.all())

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = FieldMap
        fields = ('fieldMapId', 'jobid', 'sourceColumnName', 'destColumnName', \
                   'whoCreated', 'whenCreated', 'whoUpdated',
                  'whoUpdated', 'fmeColumnType',
                  )
        read_only_fields = ('fieldMapId',)


class JobStatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = JobStatistics
        fields = ('jobStatsId', 'jobid', 'jobStatus', 'jobLabel', 'fmeServerJobId', \
                  'jobStarted', 'jobCompleted')
        read_only_fields = ('jobStatsId',)


class JobDetailedInfoSerializer(serializers.PrimaryKeyRelatedField):

    sources = SourceDataListSerializer(many=True, read_only=True)
    fieldmaps = FieldmapSerializer(many=True, read_only=True)

    class Meta:
        '''
        job details Metadata
        '''
        model = ReplicationJobs
        fields = ('jobid', 'jobStatus', 'jobLabel', 'cronStr', 'destEnvKey', 'date_created', 'date_modified', 'sources', 'fieldmaps')
        read_only_fields = ('date_created', 'date_modified')


class JobDestSerializer(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        filteredDests = None
        queryset = self.queryset
        if 'destkey' in self.context['request'].data:
            # if the destkey relates to Destinations then keep, otherwise set to None
            ProvidedEnvKey = self.context['request'].data['destkey']

            filteredDests = Destinations.objects.filter(dest_key=ProvidedEnvKey)
        if filteredDests:
            queryset = queryset.filter(dest_key=ProvidedEnvKey)
        else:
            queryset = queryset.filter()
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

    #destkey = JobDestSerializer(queryset=Destinations.objects.all(),
    #                            source='Destinations',
    #                            required=False)
    #
    # replace line below to allow for initial makemigration then swap comments
    # back.
    if ('makemigrations' in sys.argv or 'migrate' in sys.argv):
        dests = ['a', 'b']
    else:
        dests = Destinations.objects.all()
    destField = serializers.ChoiceField(choices=dests, allow_blank=True, allow_null=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = ReplicationJobs
        fields = ('jobid', 'jobStatus', 'jobLabel', 'cronStr', 'date_created',
                  'date_modified', 'sources', 'owner', 'fieldmaps', 'destField',)
        read_only_fields = ('date_created', 'date_modified', 'destEnvKey')
        depth = 1

    def create(self, validated_data):
        # validated_data {'owner': <User: spock>, u'cronStr': u'some',
        #                 u'jobStatus': u'TESTING5',
        #                 u'Destinations': <Destinations: DLV>}
        #
        originalValidation = validated_data.copy()
#         print 'validated_data', validated_data
        # use the same logic as the update,
        if 'destField' in validated_data:
            if isinstance(validated_data['destField'], Destinations):
                validated_data['destEnvKey'] = validated_data['destField']
            del validated_data['destField']

        if 'destField' in originalValidation:
            if isinstance(originalValidation['destField'], Destinations):
                originalValidation['destField'] = originalValidation['destField'].dest_key

        retval = ReplicationJobs.objects.create(**validated_data)
        retval.save()
        return originalValidation

    def update(self, instance, validated_data):
        inst = self.to_representation(validated_data)
        torep = self.to_representation(validated_data)

        if 'destField' in validated_data:
            if isinstance(validated_data['destField'], Destinations):
                if 'destEnvKey' not in validated_data:
                    validated_data['destEnvKey'] = validated_data['destField']
                    del validated_data['destField']
        # using the text value get a Destination record for that value
        # DestObj = Destinations.objects.filter(dest_key=torep['destField'])
        # validated_data['destEnvKey'] = DestObj
        retval = ReplicationJobs.objects.update(**validated_data)

        # fld: api.Destinations.dest_type {'_validators': [], 'auto_created': False, 'serialize': True, 'cached_col': Col(api_destinations, api.Destinations.dest_type), '_unique': False, 'unique_for_year': None, 'blank': False, 'help_text': u'', 'null': False, 'db_index': False, 'is_relation': False, 'unique_for_month': None, 'unique_for_date': None, 'primary_key': False, 'concrete': True, 'remote_field': None, 'max_length': 30, 'db_tablespace': u'', 'verbose_name': u'dest type', 'creation_counter': 42, 'validators': [<django.core.validators.MaxLengthValidator object at 0x02F65EF0>], 'editable': True, 'error_messages': {u'unique': u'%(model_name)s with this %(field_label)s already exists.', u'invalid_choice': u'Value %(value)r is not a valid choice.', u'blank': u'This field cannot be blank.', u'null': u'This field cannot be null.',
        #      u'unique_for_date': u'%(field_label)s must be unique for %(date_field_label)s %(lookup_type)s.'}, '_error_messages': None, '_verbose_name': None, 'name': 'dest_type', 'db_column': None, 'default': <class django.db.models.fields.NOT_PROVIDED at 0x02B11538>, 'choices': [], 'column': 'dest_type', 'model': <class 'api.models.Destinations.Destinations'>, 'attname': 'dest_type'}
        # flds (<ManyToOneRel: api.job>, <django.db.models.fields.CharField: dest_key>, <django.db.models.fields.CharField: dest_service_name>, <django.db.models.fields.CharField: dest_host>, <django.db.models.fields.IntegerField: dest_port>, <django.db.models.fields.CharField: dest_type>)
        # retval.save()
        # update: instance 7
        # update: validated_data {u'cronStr': u'blah', u'jobStatus': u'fucked', u'Destinations': <Destinations: PRD>}
        # context: <QueryDict: {u'destkey': [u'PRD'], u'cronStr': [u'blah'], u'jobStatus': [u'fucked']}>
        # status = validated_data.pop('status')
        # instance.status_id = status.id
        # ... plus any other fields you may want to update
        # instance.destEnvKey = destKey
        # instance.destkey = ''
        # return instance
        return torep

    def to_representation(self, instance):
        """
        destField: should always be a string, and it reflects the value of the
                   current destenvkey.  Want to keep it simple for getting and
                   setting destinations.  Want to be able to simply change this
                   string value, then the serializer handles the management of
                   the foreignkey update.
        """
        print 'to_representation instance:', instance, type(instance)
        #print 'destEnvKey', instance.destEnvKey
        ret = super(JobIdlistSerializer, self).to_representation(instance)
        print 'ret', ret
        print 'instance', instance
        if 'destEnvKey' in ret:
#             print 'superclass to_representation:', ret, type(ret)
#             print 'instance.destEnvKey.dest_key:', instance.destEnvKey.dest_key
            ret['destField'] = instance.destEnvKey.dest_key
        elif isinstance(ret['destField'], Destinations):
            ret['destField'] = ret['destField'].dest_key
        #  not (instance[u'destField']) or
        elif (hasattr(instance, 'destEnvKey')) and not instance.destEnvKey:
            # indicates the desetEnvKey has not been set yet, so leave as is
            pass
        else:
            ret['destField'] = instance.destEnvKey.dest_key
#         print 'ret:', ret
        # OrderedDict([('jobid', 20), ('jobStatus', u'PRETTY'), ('cronStr', u'1'), ('date_created', u'2018-06-12T23:18:34.124000Z'), ('date_modified', u'2018-06-12T23:18:34.140000Z'), ('sources', []), ('owner', u'kjnether'), ('destField', None)]) <class 'collections.OrderedDict'>
        # ret['username'] = ret['username'].lower()
        return ret


class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    # jobs = serializers.PrimaryKeyRelatedField(many=True,
    #                                         queryset=ReplicationJobs.objects.all())

    class Meta:
        """Map this serializer to the default django user model."""
        model = User
        # fields = ('id', 'username', 'jobs')
        fields = ('id', 'username', 'email')

        read_only_fields = ('authorization_directory', 'authorization_email',
                            'authorization_guid', 'authorization_id',
                            'display_name')
