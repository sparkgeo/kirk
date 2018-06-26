'''
Created on May 15, 2018

@author: kjnether
'''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from api.models.ReplicationJobs import ReplicationJobs
from api.models.Destinations import Destinations
from api.models.FieldMap import FieldMap
from api.models.Sources import Sources
from api.models.DataTypes import FMEDataTypes
from api.models.JobStatistics import JobStatistics

import pytz
import datetime

# Create your tests here.
class ModelTestCase(TestCase):
    """
    This class defines the test suite for the bucketlist model.
    """

    def setUp(self):
        """
        Define the test client and other test variables.
        """
        self.jobid = "1"
        self.user = 'spock'
        self.user = User.objects.create(username="spock")
        fixtures = ['Destination_Keywords.json']

        self.job = ReplicationJobs(jobid=self.jobid, owner=self.user)

    def test_model_can_create_a_job(self):
        """
        Test the ReplicationJobs model can create a ReplicationJobs.
        """
        # self.assertEqual(1, 1, "one doesn't equal 1")
        old_count = ReplicationJobs.objects.count()
        self.job.save()
        new_count = ReplicationJobs.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_FGDB_source(self):
        """
        Test the sources model can create a source.
        """
        old_count = Sources.objects.count()
        job = ReplicationJobs(jobid=self.jobid)
        sources = Sources(jobid=job, sourceTable='fgdbTable', sourceType='FGDB',
                          sourceDBSchema='', sourceDBName=None, sourceDBHost=None ,
                          sourceDBPort=None, sourceFilePath=r'c:\dir\dir2\somwhere\src.fgdb')
        sources.save()
        new_count = Sources.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_destination(self):
        """
        Test the Destination model can create a Destination.
        """
        old_count = Destinations.objects.count()
        job = ReplicationJobs(jobid=self.jobid)
        dests = Destinations(dest_key='DLV2', dest_service_name='ServName',
                               dest_host='dest_host', dest_port=None,
                               dest_type=r'dbase')
        dests.save()
        new_count = Destinations.objects.count()
        self.assertNotEqual(old_count, new_count)
        allDest = Destinations.objects.all()
        for dest in allDest:
            print 'dest:', dest
        
    def test_model_can_create_a_fieldmap(self):
        """
        Test the Fieldmap model can create a Fieldmap.
        """
        old_count = FieldMap.objects.count()
        fieldMap = FieldMap(sourceColumnName='COL_A', destColumnName='COL_1', 
                            fmeColumnType='fme_char', whoCreated=self.user, 
                            whoUpdated=self.user)
                             
        fieldMap.save()
        new_count = FieldMap.objects.count()
        self.assertNotEqual(old_count, new_count)
        
        
    def test_model_can_create_a_FMEDataType(self):
        """
        Test the DataType model can create a FMEDataType.
        """
        old_count = FMEDataTypes.objects.count()
        dataType = FMEDataTypes(fieldType='testchar', 
                                Description='testing description')
        dataType.save()
        new_count = FMEDataTypes.objects.count()
        self.assertNotEqual(old_count, new_count)
        dataTypes = FMEDataTypes.objects.all()
        for datatype in dataTypes:
            print 'type:', datatype
        
    def test_model_can_create_a_JobStatistic(self):
        """
        Test the Jobstatistics model can create a jobstatistic.
        """
        old_count = JobStatistics.objects.count()
        dataType = JobStatistics(jobStatus='WORKING', 
                                 fmeServerJobId=100232,
                                 jobStarted=datetime.datetime.now(pytz.UTC),
                                jobCompleted=datetime.datetime.now(pytz.UTC))
        dataType.save()
        new_count = JobStatistics.objects.count()
        self.assertNotEqual(old_count, new_count)
        
#     def test_model_can_create_a_DestinationKeyword(self):
#         old_count = JobStatistics.objects.count()
#         dataType = JobStatistics(jobStatus='WORKING', 
#                                  fmeServerJobId=100232,
#                                  jobStarted=datetime.datetime.now(pytz.UTC),
#                                 jobCompleted=datetime.datetime.now(pytz.UTC))
#         dataType.save()
#         new_count = JobStatistics.objects.count()
#         self.assertNotEqual(old_count, new_count)
         

