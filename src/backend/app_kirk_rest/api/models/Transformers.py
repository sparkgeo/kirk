'''
Created on May 25, 2018

@author: kjnether
'''
from __future__ import unicode_literals
from django.db import models
from .ReplicationJobs import ReplicationJobs
from .DataTypes import FMEDataTypes
from django.contrib.auth.models import User


class Transformers(models.Model):
    '''
    Defines the relationship between fields in the source data and the
    destination data.

    '''
    transformer_id = models.AutoField(primary_key=True)

    jobid = models.ForeignKey(ReplicationJobs, on_delete=models.SET_NULL,
                              related_name='trans_jobs', to_field='jobid',
                              null=True)
    # a text value used to describe the type of transformer this is
    transformer_type = models.CharField(max_length=64)

    # the rest of these values contain parameters that will get sent to the
    # the transformers, name will contain the name of the parameter, and
    # value will contain the name of the value.
    ts1_name = models.CharField(max_length=64, blank=True)
    ts1_value = models.CharField(max_length=64, blank=True)
    ts2_name = models.CharField(max_length=64, blank=True)
    ts2_value = models.CharField(max_length=64, blank=True)
    ts3_name = models.CharField(max_length=64, blank=True)
    ts3_value = models.CharField(max_length=64, blank=True)
    ts4_name = models.CharField(max_length=64, blank=True)
    ts4_value = models.CharField(max_length=64, blank=True)
    ts5_name = models.CharField(max_length=64, blank=True)
    ts5_value = models.CharField(max_length=64, blank=True)
    ts6_name = models.CharField(max_length=64, blank=True )
    ts6_value = models.CharField(max_length=64, blank=True)

    whoCreated = models.ForeignKey('auth.User',
                                   related_name='trans_user_created',
                                   on_delete=models.CASCADE
                                   )
    whenCreated = models.DateTimeField(auto_now_add=True)
    whoUpdated = models.ForeignKey('auth.User',
                                   related_name='trans_user_updated',
                                   on_delete=models.CASCADE)
    whenUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.transformer_id)

#     def save(self):
#         if not self.fieldMapId:
#             self.whenCreated = datetime.datetime.now()
#         super(FieldMap, self).save()
