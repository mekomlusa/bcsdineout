# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Category, Restaurant, Hour, YelpReview

admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Hour)
admin.site.register(YelpReview)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('res_id', 'name', 'yelp_url', 'favby')
    #list_filter = ('status', 'due_back')
    
    fieldsets = (
        ('Favorited', {
            'fields': ('res_id', 'name','favby',)
        }),
    )