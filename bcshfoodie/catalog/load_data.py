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
from catalog.models import Category # imports the model
with open('Category_table2017-09-12 21-28-47.193000.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = Category(name=row['Category'],res_id=row['Restaurant_id'])
        p.save()
        
