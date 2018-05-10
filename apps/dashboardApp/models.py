# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re

# Create your models here.
EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
#password must have: 8char, one uppercase letter, one number
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*[0-9])')
#names can have apostrophes or hyphens, must be letters, no numbers
NAME_REGEX = re.compile(r'^([a-zA-Z\'\-]{2,}$)')

class UserManager(models.Manager):
    def email_validator(self,postData):
        email_to_check=postData
        error=[]
        print "validating email"
        if len(email_to_check)<1:
            error='please enter an email'
        elif not EMAIL_REGEX.match(email_to_check):
            error="your email's format is incorrect"
            print error
        return error

    def name_validator(self,postData):
        name_to_check=postData
        print "validating name"
        error=[]
        if len(name_to_check)<1:
            error="Please enter a first name"
        elif not NAME_REGEX.match(name_to_check):
            error="Names must have at least 2 letters, cannot contain numbers or special characters"
        return error

    def alias_validator(self,postData):
        name_to_check=postData
        print "validating alias"
        error=[]
        if len(name_to_check)<1:
            error="Please enter an alias"
        elif not NAME_REGEX.match(name_to_check):
            error="Aliases must have at least 2 letters, cannot contain numbers or special characters"
        return error

    def pw_validator(self,postData):
        error=[]
        print "validating password"
        password_to_check=postData
        if not PASSWORD_REGEX.match(password_to_check):
            error="password must have 8 characters, and a minimum of one uppercase letter and one number"
        return error

class User(models.Model):
    firstName=models.CharField(max_length=255)
    lastName=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    userLevel=models.CharField(max_length=10)
    description=models.TextField(default="Default Description")
    objects=UserManager()

class Message(models.Model):
    message=models.TextField(default="NULL")
    created_at=models.DateTimeField(auto_now_add=True)
    messageAuthor=models.ForeignKey(User,related_name="userMessage")

class Comment(models.Model):
    comment=models.TextField(default="NULL")
    created_at=models.DateTimeField(auto_now_add=True)
    commentAuthor=models.ForeignKey(User, related_name="userComment")
    commentsMessage=models.ForeignKey(Message, related_name="messageComment")
