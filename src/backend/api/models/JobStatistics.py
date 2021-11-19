'''
Created on May 25, 2018

@author: kjnether

will include:
  - jobid
  - when started
  - when completed
  - completed status
  - features read?          - thinking can add these at a later time.
  - features written?

'''
from __future__ import unicode_literals
from django.db import models
from .ReplicationJobs import ReplicationJobs
from django.contrib.auth.models import User


class JobStatistics(models.Model):
    '''
    Defines the relationship between fields in the source data and the
    destination data.

    '''
    jobStatsId = models.AutoField(primary_key=True)
    jobid = models.ForeignKey(ReplicationJobs, on_delete=models.SET_NULL,
                              related_name='jobstatssources', to_field='jobid',
                              null=True)
    jobStatus = models.CharField(max_length=25)
    fmeServerJobId = models.IntegerField(null=True)
    jobStarted = models.DateTimeField()
    jobCompleted = models.DateTimeField()

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.jobStatsId)
