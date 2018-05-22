'''
Created on May 15, 2018

@author: kjnether
'''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from api.models.Job import Job
from api.models.Sources import Sources


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
        self.job = Job(jobid=self.jobid)

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
        
    #def test_model_can_create_a_complete_job(self):
        
        
