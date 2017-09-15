# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

import uuid 
# Create your models here.

class Restaurant(models.Model):
    """
    Model representing a restaurant (but not a specific instance of a restaurant).
    """
    res_id = models.TextField(max_length=100, help_text="Unique ID for the restaurant",default="NULL",primary_key=True)
    name = models.CharField(max_length=200)
    latitude = models.CharField(max_length=50)
    longtitude = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    image_url = models.CharField(max_length=200,default='None')
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=5)
    zipcode = models.CharField(max_length=10)
    price = models.CharField(max_length=5,default='None')
    yelp_url = models.CharField(max_length=300,default='None')
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

class Category(models.Model):
    """
    Model representing a restaurant category (e.g. Tex-Mex, Chinese)
    """
    res = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30, help_text="Enter a restaurant category (e.g. Tex-Mex, Chinese)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name    
    
class Hour(models.Model):
    """
    Model representing hours of restaurant (i.e. McDonald's on College Drive is opened 10 - 10 pm every day).
    """
    res = models.OneToOneField(Restaurant,on_delete=models.CASCADE)
    monday_start = models.IntegerField()
    monday_end = models.IntegerField()
    tuesday_start = models.IntegerField()
    tuesday_end = models.IntegerField()
    wednesday_start = models.IntegerField()
    wednesday_end = models.IntegerField()
    thursday_start = models.IntegerField()
    thursday_end = models.IntegerField()
    friday_start = models.IntegerField()
    friday_end = models.IntegerField()
    saturday_start = models.IntegerField()
    saturday_end = models.IntegerField()
    sunday_start = models.IntegerField()
    sunday_end = models.IntegerField()
    
    
    def __str__(self):
        """
        String for representing the Model object
        """
        return '%d (%d)' % (self.res.res_id,"hours")
    
class YelpReview(models.Model):
    """
    Model representing a review from Yelp.
    """
    ri = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    review = models.TextField(max_length=200, help_text="Reviewed by the Yelp User")
    review_user = models.CharField(max_length=50)
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s (%s)' % (self.ri.res_id,self.review_user)