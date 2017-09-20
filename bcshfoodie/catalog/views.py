# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Category, Restaurant, Hour, YelpReview, BookmarkBase, BookmarkRestaurant

from django.views import generic
from django.views import View

from django.contrib import auth
from django.http import HttpResponse


import random
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader

from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.models import User

from forms import SignUpForm

from django.contrib.auth import login, authenticate

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

class FavByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing restaurants favorited by current user. 
    """
    model = BookmarkRestaurant
    template_name ='restaurant_fav_by_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookmarkRestaurant.objects.filter(user_id=self.request.user)

# User signup view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration\signup.html', {'form': form})

# fav system
# link: https://evileg.com/en/post/244/
class AddBookmarkView(View):
    # This variable will set the bookmark model to be processed
    model = None

    def post(self, request, pk):
        # We need a user
        user = auth.get_user(request)
        # Trying to get a bookmark from the table, or create a new one
        bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )
    
class RmBookmarkView(View):
    # This variable will set the bookmark model to be processed
    model = None

    def post(self, request, pk):
        # We need a user
        user = auth.get_user(request)
        # Trying to get a bookmark from the table
        bookmark = self.model.objects.get(user=user, obj_id=pk)
        bookmark.delete()

        return HttpResponse(
            json.dumps({
                "result": 'deleted',
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )