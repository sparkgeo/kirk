'''
Created on May 25, 2018

@author: kjnether
'''
from __future__ import unicode_literals
from django.db import models
from .Job import Job
from django.contrib.auth.models import User
import datetime

class FieldMap(models.Model):
    '''
    Defines the relationship between fields in the source data and the
    destination data.

    '''
    # TODO: think about remodelling this to a field map object that in turn 
    #       has a set of children that describe the col -> col relationships.
    #       also should think about how the rest api will retrieve this 
    #       information.
    fieldMapId = models.AutoField(primary_key=True)
    jobid = models.ForeignKey(Job, on_delete=models.SET_NULL,
                              related_name='Jobs', to_field='jobid',
                              null=True)
    sourceColumnName = models.CharField(max_length=64)
    destColumnName = models.CharField(max_length=64)
    #TODO: make this a foreign key to the FME Data types table to ensure its 
    #      entered as a valid FME Data Type. 
    fmeColumnType = models.CharField(max_length=64)
    whoCreated = models.ForeignKey('auth.User',
                                   related_name='user_created',
                                   on_delete=models.CASCADE)
    whenCreated = models.DateTimeField(auto_now_add=True)
    whoUpdated = models.ForeignKey('auth.User',
                                   related_name='user_updated',
                                   on_delete=models.CASCADE)
    whenUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.fieldMapId)

#     def save(self):
#         if not self.fieldMapId:
#             self.whenCreated = datetime.datetime.now()
#         super(FieldMap, self).save()
