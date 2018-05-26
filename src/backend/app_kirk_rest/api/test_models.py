'''
Created on May 15, 2018

@author: kjnether
'''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from api.models.Job import Job
from api.models.Sources import Sources
from api.models.Destinations import Destinations
from api.models.FieldMap import FieldMap
from django.contrib.auth.models import User


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
        user = User.objects.create(username="spock")
        self.job = Job(jobid=self.jobid, owner=user)

    def test_model_can_create_a_job(self):
        """
        Test the bucketlist model can create a bucketlist.
        """
        # self.assertEqual(1, 1, "one doesn't equal 1")
        old_count = Job.objects.count()
        self.job.save()
        new_count = Job.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_FGDB_source(self):
        old_count = Sources.objects.count()
        job = Job(jobid=self.jobid)
        sources = Sources(jobid=job, sourceTable='fgdbTable', sourceType='FGDB',
                          sourceDBSchema='', sourceDBName=None, sourceDBHost=None ,
                          sourceDBPort=None, sourceFilePath=r'c:\dir\dir2\somwhere\src.fgdb')
        sources.save()
        new_count = Sources.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_destination(self):
        old_count = Destinations.objects.count()
        job = Job(jobid=self.jobid)
        dests = Destinations(dest_key='DLV2', dest_service_name='ServName',
                               dest_host='dest_host', dest_port=None,
                               dest_type=r'dbase')
        dests.save()
        new_count = Destinations.objects.count()
        self.assertNotEqual(old_count, new_count)
        
    def test_model_can_create_a_fieldmap(self):
        old_count = FieldMap.objects.count()
        fieldMap = FieldMap(sourceColumnName='COL_A', destColumnName='COL_1', 
                            fmeColumnType='fme_char')
        
