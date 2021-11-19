'''
Created on Jun 26, 2018

@author: kjnether
'''

from django.db import models
from django.contrib.auth.models import AbstractUser
import django.contrib.auth.validators


class User(AbstractUser):

    """
    User Model
    """
    username = models.CharField(
        error_messages={'unique': "A user with that username already exists."},
        help_text="Required. 150 characters or fewer. Letters, digits and "
                  "@/./+/-/_ only.",
        max_length=150, unique=True,
        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
        verbose_name='username'
    )

    password = models.CharField(max_length=128, blank=True, null=True)
    email = email = models.EmailField(blank=True, null=True)

    # Siteminder headers, not using for now but in case required later on if
    # integrate with openid connect.
    authorization_id = models.CharField(max_length=500, blank=True, null=True)
    authorization_guid = models.UUIDField(unique=True, default=None, null=True)
    authorization_directory = models.CharField(max_length=100, blank=True,
                                               null=True)
    authorization_email = models.EmailField(blank=True, null=True)
    display_name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        '''
        defining the table name
        '''
        app_label = 'app_auth'
        # db_table = "app_user"
        db_table = 'kirk_users'
