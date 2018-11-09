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
    jobid = models.AutoField(primary_key=True)
    jobStatus = models.CharField(max_length=20)
    jobLabel = models.CharField(max_length=100, null=True, blank=True,
                                unique=True)
    cronStr = models.CharField(max_length=25)
    destEnvKey = models.ForeignKey(Destinations, on_delete=models.SET_NULL,
                                   related_name='destEnvKey',
                                   to_field='dest_key', null=True,
                                   blank=True, editable=True)
    destTableName = models.CharField(max_length=30)
    destSchema = models.CharField(max_length=30)

    # TODO: once implement the user model change on_delete to SET_NULL
    # auth.User
    owner = models.ForeignKey('auth.User',
                              related_name='user',
                              on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.jobid)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    '''
    this receiver handles token creation immediately when a new user is
    created.
    '''
    if created:
        Token.objects.create(user=instance)
