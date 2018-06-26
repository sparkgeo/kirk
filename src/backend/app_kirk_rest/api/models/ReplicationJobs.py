'''
Created on May 15, 2018

@author: kjnether
'''
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from .Destinations import Destinations

class ReplicationJobs(models.Model):
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
                                   related_name='destEnvKey', to_field='dest_key', 
                                   null=True, blank=True, editable=True)
    #destEnvKey = models.CharField(max_length=3,null=True, blank=True, editable=True)
    
    # TODO: once implement the user model change on_delete to SET_NULL
    owner = models.ForeignKey('auth.User',  
                              related_name='user', 
                              on_delete=models.CASCADE) 
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.jobid)

        
# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

