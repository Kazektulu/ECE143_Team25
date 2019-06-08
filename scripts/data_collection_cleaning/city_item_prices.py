#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script includes the functions needed to collect the individual category/item prices for all cities in United States
#from the Numbeo Website. This data will then be used to compute the cost of living for those cities
#Details of the Website - https://www.numbeo.com/cost-of-living/
#In order to access data, their API can be utilized - https://www.numbeo.com/common/api.jsp
#
#PLEASE NOTE: In order to access this data an API Key is required. Free API Key can be requested for academic projects
#For details regarding the same refer the link given above
#
######################################################

import requests
import pandas as pd
from pandas.io.json import json_normalize

BASE_URL = "http://www.numbeo.com:8008/api/"
COUNTRY = "United States"

def api_city_list(NUMBEO_API_KEY=None, out_filename=None, file_write_enable=None):
    '''
    Function to fetch the name of all the cities (alongwith location) from the Numbeo Website using their API
    Omits cities that do not have data in the NUMBEO Database
    *** API Key is required to run this function and can be obtained from NUMBEO WEBSITE***
    
    Arguments:
        NUMBEO_API_KEY (str):
            API Key needed to access the NUMBEO Website Data using its API
            
        out_filename (str):
            Text Filename to store the final city list
            Make sure to include the complete path in the filename
            
        file_enable (bool):
            If True - write list to given filename
    
    Returns:
        (list):
            List of all cities in US present in Numbeo
        If file_enable == True:
            Text File at the location specified by the filename path
            It contains the names of the city in the NUMBEO database
    
    Our Filename: "../../raw_data/all_cities_US.txt"
    '''
    
    assert isinstance(NUMBEO_API_KEY, str), 'Input API Key is not a string'
    assert isinstance(out_filename, str), 'Input filename is not a string'
    assert isinstance(file_write_enable, bool), 'Input file_write_enable is not boolean'
    
    parameters = {'api_key':NUMBEO_API_KEY} #Parameters needed in API request
    response = requests.get(BASE_URL+"/cities",params=parameters) #Request the city information from Numbeo
    
    requested_data_json = response.json()
    try:
        requested_data_json['error'] #Check whether the response has returned an error
        print('Error Response from API')
        print(requested_data_json['error']) #If error is present, return the error and exit from the function
        assert False, 'Refer printed error'
    except:
        pass #if no error - do nothing
        
    cities_df = json_normalize(requested_data_json,'cities') #JSON Data obtained from response converted to dataframe
    cities_US_df = cities_df[cities_df.country == COUNTRY] #Retain entries of United States Only
    cities_US_list = cities_US_df.city.tolist() #List of all cities in US present in Numbeo
    
    if file_write_enable is True:
        with open(out_filename, 'w') as fp:
            for item in cities_US_list:
                fp.write("%s\n" % item)
                
    return cities_US_list
    
def api_city_item_prices(NUMBEO_API_KEY=None, city=None):
    '''
    Function to fetch the prices of all items/components for a particular city from the Numbeo Website using their API
    *** API Key is required to run this function and can be obtained from NUMBEO WEBSITE***
    
    Arguments:
        NUMBEO_API_KEY (str):
            API Key needed to access the NUMBEO Website Data using its API
            
        city (str):
            Name of the city for which data is to be requested
    
    Returns:
        (pandas.DataFrame):
            Contains average, maximum and minimum price for a maximum of 55 different items
    '''

    assert isinstance(NUMBEO_API_KEY, str), 'Input API Key is not a string'
    assert isinstance(city, str), 'Input city is not a string'
    
    city_US_list = api_city_list(NUMBEO_API_KEY, 'dummyname.txt',False)
    assert city in city_US_list, 'Given city name does not exist in Numbeo Database'
    
    parameters = {'api_key':NUMBEO_API_KEY, 'country':COUNTRY, 'city':city} #Parameters needed in API request
    response = requests.get(BASE_URL+"/city_prices",params=parameters) #Request the item/category prices for the given city
    
    requested_data_json=response.json()
    try:
        requested_data_json['error'] #Check whether the response has returned an error
        print('Error Response from API')
        print(requested_data_json['error']) #If error is present, return the error and exit from the function
        return
    except:
        pass #if no error - do nothing
    
    city_df = pd.DataFrame(requested_data_json)
    city_df = pd.concat([city_df.drop(['prices'],axis=1),city_df['prices'].apply(pd.Series)],axis=1) #Format obtained data into proper dataframe
    return city_df

def api_get_all_city_prices(NUMBEO_API_KEY=None, out_filename=None):
    '''
    Function to fetch the prices of all items/components for a all cities in US from the Numbeo Website using their API
    *** API Key is required to run this function and can be obtained from NUMBEO WEBSITE***
    
    Arguments:
        NUMBEO_API_KEY (str):
            API Key needed to access the NUMBEO Website Data using its API
            
        out_filename (str):
            Csv Filename to store the final dataframe
            Make sure to include the complete path in the filename
    
    Returns:
        Csv file at the location specified by filename
        Contains prices of items/components for all cities in US from Numbeo Database
        
    Our Filename: "../../raw_data/all_city_item_prices.csv"
    '''
    
    assert isinstance(NUMBEO_API_KEY, str), 'Input API Key is not a string'
    assert isinstance(out_filename, str), 'Input filename is not a string'
    
    city_US_list = api_city_list(NUMBEO_API_KEY, 'dummyname.txt',False) #Get list of all US cities in Numbeo Database
    city_df_dict = {}
    
    for city in city_US_list:
        city_df = api_city_item_prices(NUMBEO_API_KEY, city) #Get item/component prices for the city
        city_df_dict[city] = city_df #Append obtained dataframe to a dictionary
        
    df_cols = list(list(city_df_dict.values())[0].columns)
    city_compiled_df = pd.DataFrame(columns=df_cols)  
    
    city_compiled_df = pd.concat(city_df_dict, axis=0, ignore_index=True, sort=False) #Concatenate all dataframes together to create a single compile dataframe
    city_compiled_df.to_csv(out_filename) #Export data as csv to given filename
    
def clean_all_city_prices(in_filename=None, out_filename=None):
    '''
    Maximum number of items/components for each city are 55. 
    This function removes from the dataset all cities that have less than 55 entries to ensure consistency in the dataset
    
    Arguments:
        in_filename (str):
            Input file that contains the unclean data of prices for all cities
        out_filename (str):
            Output file that will contain the cleaned dataframe
        Make sure to include the entire path in the filename
            
    Returns:
        CSV File that contains the cleaned dataset of item/component prices for cities that have complete data only
    '''
    
    assert isinstance(in_filename, str), 'Input in_filename is not a string'
    assert isinstance(out_filename, str), 'Input out_filename is not a string'
    
    original_city_df = pd.read_csv(in_filename,index_col=0) #Read the raw all cities data file
    original_city_df_groups = original_city_df.groupby('name')
    clean_city_df_dict = {}
    
    for each,group in original_city_df_groups:
        if len(group) == 55: #Retain cities that have all 55 entries only
            clean_city_df_dict[each] = group
            
    df_cols = list(list(clean_city_df_dict.values())[0].columns)
    city_compiled_df = pd.DataFrame(columns=df_cols)  
    
    city_compiled_df = pd.concat(clean_city_df_dict, axis=0, ignore_index=True, sort=False) #Concatenate all dataframes together to create a single compile dataframe
    city_compiled_df.to_csv(out_filename) #Export data as csv to given filename
            
    
    
    
    