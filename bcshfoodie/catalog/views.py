# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Category, Restaurant, Hour, YelpReview

from django.views import generic


import random

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from django.core.paginator import Paginator

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_category=Category.objects.values('name').distinct().count()
    num_restaurant=Restaurant.objects.all().count()
    # Available restaurant in BCS area
    num_bcs_res=Restaurant.objects.filter(city__in=['College Station','Bryan']).count()
    num_yelp_review=YelpReview.objects.count()
    # todo: add list of user signed up for the site and user-generated comments.
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_category':num_category,'num_restaurant':num_restaurant,'num_bcs_res':num_bcs_res,'num_yelp_review':num_yelp_review,'num_visits':num_visits},
    )
    
class RestaurantListView(generic.ListView):
    model = Restaurant
    context_object_name = 'restaurant_list'   # your own name for the list as a template variable
    queryset = Restaurant.objects.all() # Get all restaurants in the database
    template_name = 'restaurant_list.html'  # Specify your own template name/location
    paginate_by = 25 # 25 results per page
    
class RestaurantDetailView(generic.DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'
    def get_object(self):
        return Restaurant.objects.get(res_id=self.kwargs.get("stub"))
    
class RestaurantRandomView(generic.DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'
    def get_object(self):
        count = Restaurant.objects.all().count()
        rand = random.randint(0,count)
        return Restaurant.objects.all()[rand]
    
class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'category_list'   # your own name for the list as a template variable
    #queryset = Category.objects.values('name').distinct() # Get all distinct categories in the database
    queryset = Category.objects.all().distinct('name')# Get all distinct categories in the database
    template_name = 'category_list.html'  # Specify your own template name/location
    paginate_by = 25 # 25 results per page
        
class CategoryList2View(generic.ListView):
   model = Category
   context_object_name = "crlist"
   template_name = 'category_detail.html'  # Specify your own template name/location
   def get_queryset(self):
       queryset = super(CategoryList2View, self).get_queryset()
       queryset = queryset.filter(name=self.kwargs.get("stub"))
       return queryset
   
    