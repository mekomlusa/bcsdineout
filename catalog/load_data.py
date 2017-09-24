# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 17:41:19 2017

@author: mlusa
"""

import csv
import os
path =  "D:\\my_env\\bcsdineout\\bcshfoodie\\catalog" # Set path of new directory here
os.chdir(path) # changes the directory
# update the business table!
#from catalog.models import Restaurant # imports the model
#with open('Business_table2017-09-14 21-44-00.756000.csv') as csvfile:
#    reader = csv.DictReader(csvfile)
#    for row in reader:
#        p = Restaurant(res_id=row['Restaurant_id'],name=row['Name'],latitude=row['Latitude'],
#                       longtitude=row['Longtitude'],phone=row['Phone'],image_url=row['Image_url'],
#                       address=row['Address'],city=row['City'],state=row['State'],zipcode=row['Zip'],
#                       price=row['Price'],yelp_url=row['Yelp_url'])
#        p.save()

# update the catalog table!
#from catalog.models import Category # imports the model
#with open('Category_table2017-09-12 21-28-47.193000.csv') as csvfile:
#    reader = csv.DictReader(csvfile)
#    for row in reader:
#        p = Category(name=row['Category'],res_id=row['Restaurant_id'])
#        p.save()
        
# update the yelp review table!
#from catalog.models import YelpReview,Restaurant # imports the model
#with open('Review_table2017-09-17 20-23-19.424000.csv') as csvfile:
#    reader = csv.DictReader(csvfile)
#    for row in reader:
#        p = YelpReview(ri=Restaurant(row['Restaurant_id']),review_user=row['Review_user'],review=row['Review_text'],review_url=row['Review_url'])
#        p.save()
        
# update the hours table!
from catalog.models import Hour,Restaurant # imports the model
with open('Hours_table2017-09-12 21-29-56.739000.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = Hour(res=Restaurant(row['Restaurant_id']),
                 monday_start=row['hours_open_monday'],monday_end=row['hours_close_monday'],
                 tuesday_start=row['hours_open_tuesday'],tuesday_end=row['hours_close_tuesday'],
                 wednesday_start=row['hours_open_wednesday'],wednesday_end=row['hours_close_wednesday'],
                 thursday_start=row['hours_open_thursday'],thursday_end=row['hours_close_thursday'],
                 friday_start=row['hours_open_friday'],friday_end=row['hours_close_friday'],
                 saturday_start=row['hours_open_saturday'],saturday_end=row['hours_close_saturday'],
                 sunday_start=row['hours_open_sunday'],sunday_end=row['hours_close_sunday'])
        p.save()
        
