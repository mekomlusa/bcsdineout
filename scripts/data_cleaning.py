# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 16:16:58 2017

@author: mlusa
"""

# To extract the details and saved into a data frame
# Category

import pandas as pd

business = pd.DataFrame(columns=['id', 'name', 'categories', 'latitude', 'longtitude', 'phone', 'hours_monday',
                                 'hours_tuesday','hours_wednesday','hours_thursday','hours_friday','hours_saturday',
                                 'hours_sunday','image_url','address_1','address_2','address_3','city','state',
                                 'zip_code','price','yelp_rating','yelp_url','yelp_review_count'])


s = ''   
if type(l[0]['categories']) == list:
    for i in l[0]['categories']:
        s=s+i['alias']+","