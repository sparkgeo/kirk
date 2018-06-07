'''
Created on May 25, 2018

@author: kjnether

These are defined for each new version of FME. This lists the types for FME 
2017
http://docs.safe.com/fme/2017.1/html/FME_Desktop_Documentation/FME_Workbench/!FeatureTypeProperties/FME-Data-Types.htm

'''
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class FMEDataTypes(models.Model):
    '''
    Defines the relationship between fields in the source data and the
    destination data.

    '''
    fieldTypeId = models.AutoField(primary_key=True)
    fieldType = models.CharField(max_length=30)
    Description = models.TextField()

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.fieldTypeId)
