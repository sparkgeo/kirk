'''
Created on May 16, 2018

@author: kjnether
'''

# Add these imports at the top
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.test import TestCase
from api.models.Job import Job
from api.models.Sources import Sources


# Define this after the ModelTestCase
class JobViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        job_data = {'jobStatus': 'TESTING5',
                    'cronStr': 'some'}
        #'destEnvKey': 'DLV',
        #job_data = {'jobid', 7}
        self.response = self.client.post(
            reverse('job_create'),
            job_data,
            format="json")

    def test_api_can_create_a_job(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        
    def test_api_can_get_a_job(self):
        """Test the api can get a given bucketlist."""
        joblist = Job.objects.get(jobStatus='TESTING5')
        #print 'joblist', joblist, type(joblist)
        #print 'joblist.jobid', joblist.jobid
        response = self.client.get(
            reverse('job_details',
            kwargs={'jobid': joblist.jobid}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, joblist)


    def test_api_can_update_a_job(self):
        """Test the api can update a given bucketlist."""
        jobs =  Job.objects.get(jobStatus='TESTING5')
        change_bucketlist = {'jobStatus': 'TESTING6',
                             'cronStr': 'required'}
        res = self.client.put(
            reverse('job_details', kwargs={'jobid': jobs.jobid}),
            change_bucketlist, format='json'
        )
        print res.content

        self.assertEqual(res.status_code, status.HTTP_200_OK)
 
    def test_api_can_delete_a_job(self):
        """Test the api can delete a bucketlist."""
        jobList = Job.objects.get(jobStatus = 'TESTING5')
        response = self.client.delete(
            reverse('job_details', kwargs={'jobid': jobList.jobid}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
         
    
class SourceViewTestCase(TestCase):
    """Define the test client and other test variables."""
     
    def setUp(self):
        self.client = APIClient()
         
        source_data = {
                       'sourceTable':'fgdbTable',
                       'sourceType':'FGDB',
                       'sourceFilePath':r'c:\dir\dir2\somwhere\src.fgdb'}
        self.response = self.client.post(
            reverse('source_create'),
            source_data,
            format="json")
     
    def test_api_can_create_a_source(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
 
#     def test_api_can_get_a_source(self):
#         """Test the api can get a given source dataset definition."""
#         sourceList = Sources.objects.get(sourceid=1)
#         #print 'sourceList', sourceList, type(sourceList)
#         #print 'sourceList.sourceid', sourceList.sourceid
#         response = self.client.get(
#             reverse('source_details',
#             kwargs={'sourceid': sourceList.sourceid}), format="json")
#   
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertContains(response, sourceList)
#  
#     def test_api_can_update_a_source(self):
#         """Test the api can update a given source."""
#         sources =  Sources.objects.get(sourceid=1)
#         change_source_list = {'sourceTable': 'TESTCHANGE'}
#         res = self.client.put(
#             reverse('source_details', kwargs={'sourceid': sources.sourceid}),
#             change_source_list, format='json'
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         
#     def test_api_can_delete_a_source(self):
#         """Test the api can delete a source."""
#         sourceList = Sources.objects.get(sourceid=1)
#         response = self.client.delete(
#             reverse('source_details', kwargs={'sourceid': sourceList.sourceid}),
#             format='json',
#             follow=True)
#         self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

