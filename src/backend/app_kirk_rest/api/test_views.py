'''
Created on May 16, 2018

@author: kjnether
'''

# Add these imports at the top
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.test import TestCase
from api.models.ReplicationJobs import ReplicationJobs
from api.models.Sources import Sources
from api.models.JobStatistics import JobStatistics
from api.models.FieldMap import FieldMap
from django.contrib.auth.models import User
import datetime
import pytz
import os.path
from api.models.DataTypes import FMEDataTypes


# Define this after the ModelTestCase
class JobViewTestCase(TestCase):
    """Test suite for the api views."""
    fixtures = ['Destination_Keywords.json']

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        user = User.objects.create(username="spock")
        self.client.force_authenticate(user=user)

        # from api.models.Destinations import Destinations
        # dests = Destinations.objects.all()
        # print 'dests:', dests
        # for dest in dests:
        #    print 'dest', dest

        job_data = {'jobStatus': 'TESTING5',
                    'cronStr': 'some',
                    'owner': user.id,
                    'destField': 'DLV'}
        self.response = self.client.post(
            reverse('job_create'),
            job_data,
            format="json")
        #print 'response content', self.response.content

    def test_api_can_create_a_job(self):
        """Test the api has replication job creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        #print 'job created!'

    def test_api_can_get_a_job(self):
        """Test the api can get a given replication job."""
        joblist = ReplicationJobs.objects.get(jobStatus='TESTING5')
        # print 'joblist', joblist, type(joblist)
        # print 'joblist.jobid', joblist.jobid
        response = self.client.get(
            reverse('job_details',
            kwargs={'jobid': joblist.jobid}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, joblist)

    def test_api_can_update_a_job(self):
        """Test the api can update a given replication job."""
        jobs = ReplicationJobs.objects.get(jobStatus='TESTING5')
        change_bucketlist = {'jobStatus': 'TESTING6',
                             'cronStr': 'required',
                             'destField': 'TST'}
        res = self.client.put(
            reverse('job_details', kwargs={'jobid': jobs.jobid}),
            change_bucketlist, format='json'
        )
        #print 'update result', res.content

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_a_job(self):
        """Test the api can delete a replication job."""
        #print 'testing deleting'
        jobList = ReplicationJobs.objects.get(jobStatus='TESTING5')
        #print 'jobList', jobList
        response = self.client.delete(
            reverse('job_details', kwargs={'jobid': jobList.jobid}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class SourceViewTestCase(TestCase):
    """Define the test client and other test variables."""

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="spock")
        self.client.force_authenticate(user=user)
        source_data = {
                       'sourceTable':'fgdbTable',
                       'sourceType':'FGDB',
                       'sourceFilePath':r'c:\dir\dir2\somwhere\src.fgdb'
                       }
        self.response = self.client.post(
            reverse('source_create'),
            source_data,
            format="json")
        # print 'response: ', self.response.content

    def test_api_can_create_a_source(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_source(self):
        """Test the api can get a given source dataset definition."""
        sourceList = Sources.objects.get(sourceid=1)
        # print 'sourceList', sourceList, type(sourceList)
        # print 'sourceList.sourceid', sourceList.sourceid
        response = self.client.get(
            reverse('source_details',
            kwargs={'sourceid': sourceList.sourceid}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, sourceList)

    def test_api_can_update_a_source(self):
        """Test the api can update a given source."""
        sources = Sources.objects.get(sourceid=1)
        change_source_list = {'sourceTable': 'TESTCHANGE'}
        res = self.client.put(
            reverse('source_details', kwargs={'sourceid': sources.sourceid}),
            change_source_list, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_a_source(self):
        """Test the api can delete a source."""
        sourceList = Sources.objects.get(sourceid=1)
        response = self.client.delete(
            reverse('source_details', kwargs={'sourceid': sourceList.sourceid}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class FieldMapViewTestCase(TestCase):
    fixtures = ['fme_data_types.json']


    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="spock")
        job_data = {'jobStatus': 'TESTING5',
                    'cronStr': 'some',
                    'owner': user.id,
                    'destField': 'DLV'}
        
        fmeColTypes = FMEDataTypes.objects.all()
        print 'fmeColTypes', fmeColTypes
        print 'fmeColType', fmeColTypes[0].fieldType
        jobs = ReplicationJobs.objects.create(jobStatus='Testing', cronStr='test', 
                                              owner=user)
        self.fieldType = fmeColTypes[0].fieldTypeId
        self.client.force_authenticate(user=user)
        fldMapData = { 'sourceColumnName':'COLA',
                       'destColumnName':'COLUMN_A',
                       'fmeColumnType':fmeColTypes[0].fieldTypeId, 
                       "whoUpdated": user.id,
                       "whoCreated": user.id }
        self.response = self.client.post(
            reverse('fieldmap_create'),
            fldMapData,
            format="json")

    def test_api_can_create_a_fieldmap(self):
        """Test the api has fieldmap creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_fieldmap(self):
        """Test the api can get a given source dataset definition."""
        fldmapList = FieldMap.objects.all()
        print 'fldmapList', fldmapList
        print 'fldmapList[0]', fldmapList[0], type(fldmapList[0])
        print 'value: ', fldmapList[0].fieldMapId
        param = fldmapList[0].fieldMapId
        response = self.client.get(
            reverse('fieldmap_details',
            kwargs={'fieldMapId': param}),
            format="json")
        print 'response', response.content

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, fldmapList[0])

# TODO: check on the rest of the views

# class JobStatisticsTestCase(TestCase):
# 
#     def setUp(self):
#         self.client = APIClient()
#         user = User.objects.create(username="spock")
#         self.client.force_authenticate(user=user)
#         fldMapData = {
#                        'jobStatus':'DINNER',
#                        'fmeServerJobId': 100123,
#                        "jobStarted": datetime.datetime.now(pytz.UTC),
#                        "jobCompleted": datetime.datetime.now(pytz.UTC) }
#         self.response = self.client.post(
#             reverse('jobstats_create'),
#             fldMapData,
#             format="json")
#         # print 'response: ', self.response.status_code
#         # print 'response content:', self.response.content
# 
#     def test_api_can_create_a_jobstat(self):
#         """Test the api has JobStatistics creation capability."""
#         self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
# 
#     def test_api_can_get_a_jobstat(self):
#         """Test the api can get a given jobstat dataset definition."""
#         jobStatList = JobStatistics.objects.get(jobStatsId=1)
#         # print 'sourceList', sourceList, type(sourceList)
#         # print 'sourceList.sourceid', sourceList.sourceid
#         response = self.client.get(
#             reverse('jobstats_details',
#             kwargs={'jobStatsId': jobStatList.jobStatsId}), format="json")
# 
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertContains(response, jobStatList)


class DestinationsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="spock")
        self.client.force_authenticate(user=user)
        fldMapData = {
                       'jobStatus':'DINNER',
                       'fmeServerJobId': 100123,
                       "jobStarted": datetime.datetime.now(pytz.UTC),
                       "jobCompleted": datetime.datetime.now(pytz.UTC) }
        self.response = self.client.post(
            reverse('jobstats_create'),
            fldMapData,
            format="json")
        # print 'response: ', self.response.status_code
