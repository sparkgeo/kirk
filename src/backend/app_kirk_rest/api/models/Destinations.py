'''
Created on May 24, 2018

@author: kjnether
'''

from __future__ import unicode_literals
from django.db import models


class Destinations(models.Model):
    '''
    Defines the destinations, uses key words in the job to define the destinations
    Keyword relates to this table.
    '''
    dest_key = models.CharField(max_length=3, primary_key=True)
    dest_service_name = models.CharField(max_length=30, blank=False, null=False)
    dest_host = models.CharField(max_length=30, blank=False, null=False)
    dest_port = models.IntegerField(blank=True, null=True)
    # for now everything will be oracle, but leaves door open for other config
    dest_type = models.CharField(max_length=30)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.dest_key)
    
