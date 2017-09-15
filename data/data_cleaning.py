# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 16:16:58 2017

@author: mlusa
"""

# To extract the details and saved into data frames
# Category

import pandas as pd
import ast
import datetime
import os

all_res_str = []
all_res_json = []
dir = os.getcwd()

category = pd.DataFrame(columns=['Restaurant_id','Category'])
operation_hours = pd.DataFrame(columns=['Restaurant_id','hours_open_sunday','hours_open_monday',
                                 'hours_open_tuesday','hours_open_wednesday','hours_open_thursday','hours_open_friday',
                                 'hours_open_saturday','hours_close_sunday','hours_close_monday',
                                 'hours_close_tuesday','hours_close_wednesday','hours_close_thursday','hours_close_friday',
                                 'hours_close_saturday'
                                ])
business = pd.DataFrame(columns=['Restaurant_id', 'Name', 'Latitude', 'Longtitude', 'Phone', 'Image_url','Address','City','State',
                                 'Zip','Price','Yelp_url'])
reviews = pd.DataFrame(columns=['Restaurant_id','Review_user','Review_text','Review_url'])

# read all files into a list
def load_restaurants(filename):
    # To retrieve the data next time without directly quering Twitter, uncomment the lines below
    # (don't run get_all_followers() then)
    try:
        fhand = open(filename,"r")
        for line in fhand:
            all_res_str.append(line.rstrip())
        print "Successfully load all restaurants (json) in the file!"
        print ""
    except IOError:
        print "Sorry, the file does not exist on the disk. Please try again."
        filename = raw_input("Where did you save your file?: ")
        load_restaurants(filename)
        
# clean up the json file
def convert_to_json(listname):
    for item in all_res_str:
        if "error" not in item:
            all_res_json.append(ast.literal_eval(item))
            
# further cleanup for the dataframe restaurant
def restaurant(df):
    for item in all_res_json:
        Restaurant_id = item.get('id','')
        Name = item.get('name','')
        Latitude = str(item['coordinates'].get('latitude',''))
        Longtitude = str(item['coordinates'].get('longitude',''))
        Phone = item.get('phone','')
        Image_url = item.get('image_url','')
        Address_1 = item['location'].get('address1','')
        Address_2 = item['location'].get('address2','')
        Address_3 = item['location'].get('address3','')
        Address = xstr(Address_1) + " " + xstr(Address_2) + " " + xstr(Address_3)
        City = item['location'].get('city','')
        State = item['location'].get('state','')
        Zip = item['location'].get('zip_code','')
        Price = item.get('price','')
        Yelp_url = item.get('url','')
        df.loc[len(df)+1]=[Restaurant_id,Name,Latitude,Longtitude,Phone,Image_url,Address,City,State,Zip,Price,Yelp_url]
    
# to convert None string. A little function from StackOverflow.
def xstr(s):
    if s is None:
        return ''
    return str(s)
    
# further cleanup for the dataframe category
def categories(df):
    for item in all_res_json:
        Restaurant_id = item['id']
        for cat in item['categories']:
            df.loc[len(df)+1]=[Restaurant_id,cat['alias']]
        
# further cleanup for the dataframe ops_hours
def ops_hours(df):
    for item in all_res_json:
        Restaurant_id = item['id']
        
        hours_open_sunday = ''
        hours_open_monday = ''
        hours_open_tuesday = ''
        hours_open_wednesday = ''
        hours_open_thursday = ''
        hours_open_friday = ''
        hours_open_saturday = ''
        hours_close_sunday = ''
        hours_close_monday = ''
        hours_close_tuesday = ''
        hours_close_wednesday = ''
        hours_close_thursday = ''
        hours_close_friday = ''
        hours_close_saturday = ''
        
        if item.get('hours','') <> '':
            for d in item['hours'][0]['open']:
                if d.get('day') == 0:
                    hours_open_sunday = d.get('start','')
                    hours_close_sunday = d.get('end', '')
                    continue
                elif d.get('day') == 1:
                    hours_open_monday = d.get('start','')
                    hours_close_monday = d.get('end', '')
                    continue
                elif d.get('day') == 2:
                    hours_open_tuesday = d.get('start','')
                    hours_close_tuesday = d.get('end', '')
                    continue
                elif d.get('day') == 3:
                    hours_open_wednesday = d.get('start','')
                    hours_close_wednesday = d.get('end', '')
                    continue
                elif d.get('day') == 4:
                    hours_open_thursday = d.get('start','')
                    hours_close_thursday = d.get('end', '')
                    continue
                elif d.get('day') == 5:
                    hours_open_friday = d.get('start','')
                    hours_close_friday = d.get('end', '')
                    continue
                else:
                    hours_open_saturday = d.get('start','')
                    hours_close_saturday = d.get('end', '')
                    continue
        else:
            print Restaurant_id,'has no operation hour available. Skipping...'
            continue
            
        df.loc[len(df)+1]=[Restaurant_id,hours_open_sunday,hours_open_monday,
        hours_open_tuesday,hours_open_wednesday,hours_open_thursday,hours_open_friday,
        hours_open_saturday,hours_close_sunday,hours_close_monday,
        hours_close_tuesday,hours_close_wednesday,hours_close_thursday,hours_close_friday,
        hours_close_saturday]

# further cleanup for the dataframe business_review        
def review(df):
    review_text = ""
    review_url = ""
    review_user = ""
    for item in all_res_str:
        if "error" not in item:
            Restaurant_id = item.split(',')[0]
            json = ast.literal_eval(item[item.index(item.split(',')[1]):])
            for rating in json['reviews']:
                review_user = rating['user']['name']
                review_text = rating['text']
                review_url = rating['url']
                df.loc[len(df)+1]=[Restaurant_id,review_user,review_text,review_url]
        
        
            
def output_file(df, fn):
    # Output the dataframes.
    today = datetime.datetime.today()
    outputname = fn+str(today).replace(':','-')+".csv"
    df.drop_duplicates(inplace=True)
    if len(df) > 0:
        df.to_csv(outputname,sep=',', na_rep=" ", encoding='utf-8', index_label=False, index=False) 
        print "The details of the given dataframe has been saved under "+dir+" as "+outputname
        
def main():
    load_restaurants("json_restaurant_list_2017-09-12 17-25-03.962000.csv")
    load_restaurants("json_restaurant_list_2017-09-12 17-32-48.300000.csv")
    load_restaurants("json_restaurant_list_2017-09-12 17-52-00.274000.csv")
    load_restaurants("json_restaurant_list_2017-09-12 17-59-41.852000.csv")
#    load_restaurants("json_restaurant_review_2017-09-13 14-12-00.154000.csv")
#    load_restaurants("json_restaurant_review_2017-09-13 14-32-50.790000.csv")
    print "Converting to json type..."
    convert_to_json(all_res_str)
    print "Extracting business table..."
    restaurant(business)
#    print "Extracting categories table..."
#    categories(category)
#    print "Extracting operation hours table..."
#    ops_hours(operation_hours)
#    print "Extracting the review table..."
#    review(reviews)
    print "writing out the data frames..."
    output_file(business,"Business_table")
#    output_file(category,"Category_table")
#    output_file(operation_hours,"Hours_table")
#    output_file(reviews,"Review_table")
    
    
if __name__ == '__main__':
  main()
  
