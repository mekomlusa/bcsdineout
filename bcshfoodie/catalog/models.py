# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

from django.db.models.aggregates import Count

from random import randint

from datetime import datetime

from django.contrib.auth.models import User
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
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('restaurant-detail', args=[str(self.res_id)])
    
    class Meta:
        """
        To define user permissions here.
        """
        permissions = (("can_mark_fav", "Set restaurant as favorited"),
                       ("can_mark_unfav", "Remove restaurant from favorite list"),
                       ("can_add_note", "Add a note to a restaurant"),
                       ("can_delete_note","Remove a note to a restaurant"))

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
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('category-list-2', args=[str(self.name)])
      
def formattedHours(string):
    """
    Return formatted hours.
    """
    if string != '':
        return str(datetime.strptime(string, '%H%M').time())[:-3]
    else:
        return "None"
        
class Hour(models.Model):
    """
    Model representing hours of restaurant (i.e. McDonald's on College Drive is opened 10 - 10 pm every day).
    """
    res = models.OneToOneField(Restaurant,on_delete=models.CASCADE)
    monday_start = models.CharField(max_length=5,default='None')
    monday_end = models.CharField(max_length=5,default='None')
    tuesday_start = models.CharField(max_length=5,default='None')
    tuesday_end = models.CharField(max_length=5,default='None')
    wednesday_start = models.CharField(max_length=5,default='None')
    wednesday_end = models.CharField(max_length=5,default='None')
    thursday_start = models.CharField(max_length=5,default='None')
    thursday_end = models.CharField(max_length=5,default='None')
    friday_start = models.CharField(max_length=5,default='None')
    friday_end = models.CharField(max_length=5,default='None')
    saturday_start = models.CharField(max_length=5,default='None')
    saturday_end = models.CharField(max_length=5,default='None')
    sunday_start = models.CharField(max_length=5,default='None')
    sunday_end = models.CharField(max_length=5,default='None')
    
    
    def __str__(self):
        """
        String for representing the Model object
        """
        return '%d (%d)' % (self.res.res_id,"hours")
    
    def hoursOfOpearation(self):
        """
        Return hours of operations in human readable format.
        """
        return "Monday: %s - %s\nTuesday: %s - %s\n Wednesday: %s - %s\n Thursday: %s - %s\n Friday: %s - %s\n Saturday: %s - %s\n Sunday: %s - %s" % (formattedHours(self.monday_start), formattedHours(self.monday_end),
                 formattedHours(self.tuesday_start), formattedHours(self.tuesday_end),
                 formattedHours(self.wednesday_start), formattedHours(self.wednesday_end),
                 formattedHours(self.thursday_start), formattedHours(self.thursday_end),
                 formattedHours(self.friday_start), formattedHours(self.friday_end),
                 formattedHours(self.saturday_start), formattedHours(self.saturday_end),
                 formattedHours(self.sunday_start), formattedHours(self.sunday_end))

        
class YelpReview(models.Model):
    """
    Model representing a review from Yelp.
    """
    ri = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    review = models.TextField(max_length=200, help_text="Reviewed by the Yelp User")
    review_user = models.CharField(max_length=50)
    review_url = models.CharField(max_length=350,default='None')
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        #return '%s (%s)' % (self.ri.res_id,self.review_user)
        return '%s' % (self.review_user)
    
    def reviewtext(self):
        """
        Printing out the review object in a short-hand list when called by the Restaurant object.
        """
        return '%s : %s' % (self.review_user, self.review)
    
    def get_url(self):
        """
        Returns the url to access a particular review.
        """
        return '%s' % (self.review_url)

# bookmark system
class BookmarkBase(models.Model):
    class Meta:
        abstract = True
 
    user = models.ForeignKey(User, verbose_name="User")
 
    def __str__(self):
        return self.user.username

class BookmarkRestaurant(BookmarkBase):
    class Meta:
        db_table = "bookmark_restaurant"
 
    obj = models.ForeignKey(Restaurant, verbose_name="Restaurant")
    
    def get_bookmark_count(self):
        return self.bookmarkrestaurant_set().all().count()