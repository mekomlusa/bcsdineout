# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Category, Restaurant, Hour, YelpReview, BookmarkBase, BookmarkRestaurant, NoteBase, NoteRestaurant, URRestaurant, URBase

from django.views import generic
from django.views import View

from django.contrib import auth
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
   
import random
import json

from django.shortcuts import render, redirect, get_object_or_404, render_to_response

from django.template import RequestContext, loader

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.models import User

from . forms import SignUpForm, NoteForm

from django.contrib.auth import login, authenticate

from django.core.urlresolvers import reverse

from itertools import chain

from django.db.models import Q

import operator

import re

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
    """
    View function to display all restaurants on file.
    """
    model = Restaurant
    context_object_name = 'restaurant_list'   # your own name for the list as a template variable
    queryset = Restaurant.objects.all() # Get all restaurants in the database
    template_name = 'restaurant_list.html'  # Specify your own template name/location
    paginate_by = 25 # 25 results per page
    
class RestaurantDetailView(generic.DetailView):
    """
    View function to display specific details of a restaurant instance.
    """
    model = Restaurant
    template_name = 'restaurant_detail.html'
    def get_object(self):
        return Restaurant.objects.get(res_id=self.kwargs.get("stub"))
    
    def get_context_data(self, **kwargs):
        context = super(RestaurantDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            queryset2 = URRestaurant.objects.filter(user_id=self.request.user,obj_id=self.kwargs.get("stub"))
            context['notes'] = queryset2
        return context
    
class RestaurantRandomView(generic.DetailView):
    """
    View function for the random restaurant picker.
    """
    model = Restaurant
    # the template is essentially the same as the restaurant detail page but with a shuffle button
    template_name = 'restaurant_detail_rand.html'
    def get_object(self):
        count = Restaurant.objects.all().count()
        rand = random.randint(0,count)
        return Restaurant.objects.all()[rand]
    
class CategoryListView(generic.ListView):
    """
    View function to display all categories on file.
    """
    model = Category
    context_object_name = 'category_list'   # your own name for the list as a template variable
    queryset = Category.objects.all().distinct('name')# Get all distinct categories in the database
    template_name = 'category_list.html'  # Specify your own template name/location
    paginate_by = 25 # 25 results per page
        
class CategoryList2View(generic.ListView):
   """
   Display a list of restaurants that belong to a specific category.
   """
   model = Category
   context_object_name = "crlist"
   template_name = 'category_detail.html'  # Specify your own template name/location
   paginate_by = 25
   def get_queryset(self):
       queryset = super(CategoryList2View, self).get_queryset()
       queryset = queryset.filter(name=self.kwargs.get("stub"))
       return queryset

class FavByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing restaurants favorited by current user. 
    """
    model = URRestaurant
    template_name ='restaurant_fav_by_user.html'
    paginate_by = 10
    
    def get_queryset(self):
         return URRestaurant.objects.filter(user_id=self.request.user)


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
    return render(request, 'registration/signup.html', {'form': form})

# fav system
# reference link: https://evileg.com/en/post/244/
# rewritten 9/28 to accomdate the new user-restaurant syste,
def bmpost(request, pk):
    # Get user information
    user = auth.get_user(request)
    # Trying to get a bookmark from the table, or create a new one
    # if the bookmark instance has already been created in the system and user has already liked it, abort the action
    if URRestaurant.objects.filter(user=user, obj_id=pk).exists():
        if URRestaurant.objects.get(user=user, obj_id=pk).like == True:
            return JsonResponse({
            'success': False, 
            'err_code': 'Entry_existed', 
            })
        # else mark the restaurant as favorited by the user
        ulike = URRestaurant.objects.get(user=user, obj_id=pk)
        ulike.like = True
        ulike.save()
    else:
        # this is a new restaurant that user would like to bookmark!
        URRestaurant.objects.create(user=user, obj_id=pk, like=True)

    return JsonResponse({
        'success': True, 
        'err_code': 'Pass', 
    })
    
def rmbookmark(request, pk):
    # Get user information
    user = auth.get_user(request)
    # Trying to get a bookmark from the table
    # need to check if the bookmark exists in the system already or not
    if not URRestaurant.objects.filter(user=user, obj_id=pk).exists():
        return JsonResponse({
        'success': False, 
        'err_code': 'Entry_not_existed', 
    })
    # if user has created an entry for note but not for bookmark
    elif URRestaurant.objects.filter(user=user, obj_id=pk).exists():
        if URRestaurant.objects.get(user=user, obj_id=pk).like == False:
            return JsonResponse({
        'success': False, 
        'err_code': 'Entry_not_existed', 
    })

    # otherwise this is an existing restaurant that user would like to remove!
    ulike = URRestaurant.objects.get(user=user, obj_id=pk)
    ulike.like = False
    # check to see if there is a need to remove the record
    if ulike.note != "None":
        ulike.save()
    else:
        ulike.delete()

    return JsonResponse({
        'success': True, 
        'err_code': 'Pass', 
    })
    
# note system
def addNote(request, pk):
    # check to see if there is already a note existed in the system
    if URRestaurant.objects.filter(user=request.user, obj_id=pk).exists():
        if len(URRestaurant.objects.get(user=request.user, obj_id=pk).note) > 0 and URRestaurant.objects.get(user=request.user, obj_id=pk).note != 'None':
                return JsonResponse({
                'success': False, 
                'err_code': 'Note_existed', 
            })
    
    res = get_object_or_404(Restaurant, pk=pk)
    # user has never added a note to this restaurant nor favorited it. This will be a brand new record.
    if not URRestaurant.objects.filter(user=request.user, obj_id=pk).exists():
        form = NoteForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            u = request.user
            comment.user = u
            comment.obj = res
            comment.save()
            return redirect('my-fav-res')
    else:
        # somehow user has some operations on this restaurant before
        record = URRestaurant.objects.get(user=request.user, obj_id=pk)
        form = NoteForm(request.POST, instance=record)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('my-fav-res')            
    return render(request, 'notes.html', 
                              { 'form': form, 'restaurant':res, 'user':request.user })
    
def updateNote(request, pk):
    # Check to see if there is an existing note
    if not URRestaurant.objects.filter(user=request.user, obj_id=pk).exists():
            return JsonResponse({
            'success': False, 
            'err_code': 'Note_non_existed', 
        })
    elif URRestaurant.objects.filter(user=request.user, obj_id=pk).exists():
        if URRestaurant.objects.get(user=request.user, obj_id=pk).note == 'None':
                return JsonResponse({
                'success': False, 
                'err_code': 'Note_non_existed', 
            })
    
    res = get_object_or_404(Restaurant, pk=pk)
    # There is an existing note and the user indeed would like to update it.
    existing_note = URRestaurant.objects.get(user=request.user, obj_id=pk)
    form = NoteForm(request.POST or None, instance=existing_note)
    if form.is_valid():
        comment = form.save(commit=False)
        u = request.user
        comment.user = u
        comment.obj = res
        comment.save()
        return redirect('my-fav-res')
    return render(request, 'notes.html', 
                              { 'form': form, 'restaurant':res, 'user':request.user })
    
def deleteNote(request, pk):
    # Check to see if there is an existing note.
    if not URRestaurant.objects.filter(user=request.user, obj_id=pk).exists():
            return JsonResponse({
            'success': False, 
            'err_code': 'Note_non_existed', 
        })
    elif URRestaurant.objects.filter(user=request.user, obj_id=pk).exists():
        if len(URRestaurant.objects.get(user=request.user, obj_id=pk).note) > 0 and URRestaurant.objects.get(user=request.user, obj_id=pk).note == 'None':
                return JsonResponse({
                'success': False, 
                'err_code': 'Note_non_existed', 
            })
    # set the note to be None.
    existing_note = URRestaurant.objects.get(user=request.user, obj_id=pk)
    existing_note.note = "None"
    # check to see if there is a need to remove the record
    if existing_note.like == True:
        existing_note.save()
    else:
        existing_note.delete()
    return JsonResponse({
        'success': True, 
        'err_code': 'Pass', 
    })
    
class CommunityView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing restaurants favorited by current user. 
    """
    model = URRestaurant
    template_name ='community.html'
    paginate_by = 25
    
    def get_queryset(self):
         return URRestaurant.objects.filter(~Q(user_id=self.request.user)).order_by('id')

       
def search_form(request):
    """
    A simple view handler that redirects user to the search page.
    """
    return render(request, 'searchf.html')

def search2(request):
    """
    A simple search function. Could include complicated logic in the future.
    """
    if 'q' in request.GET:
        query = request.GET.get('q')
        if query:
            query_list = query.split()
            result = Restaurant.objects.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(address__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(city__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(category__name__icontains=q) for q in query_list))
            ).distinct()
            paginator = Paginator(result, 15)
            page = request.GET.get('page', 1)
            result = paginator.page(page)
            return render(request, 'results.html', {'results': result, 'query': '?q=%s' % query, 'term': query})
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)