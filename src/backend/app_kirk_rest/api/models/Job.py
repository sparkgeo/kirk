'''
Created on May 15, 2018

@author: kjnether
'''
from __future__ import unicode_literals
from django.db import models
from .Destinations import Destinations

class Job(models.Model):
    '''
    Sources
    ----------------
    jobid: foreign key
    sourceTable: source table
    jobStatus: the status of the job
        - PENDING
        - COMPLETE
        - PROCESSING
    '''
    #DESTINATION_CHOICES = ()
    
    jobid = models.AutoField(primary_key=True)
    jobStatus = models.CharField(max_length=20)
    cronStr = models.CharField(max_length=25)
    destEnvKey = models.ForeignKey(Destinations, on_delete=models.SET_NULL, 
                                   related_name='destkey', to_field='dest_key', 
                                   null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.jobid)
