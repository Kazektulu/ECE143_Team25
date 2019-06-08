#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script includes the functions needed to collect the raw quality of life index data
#from the Numbeo Website.
#Details of the Website - https://www.numbeo.com/quality-of-life/
#In order to access data, their API can be utilized - https://www.numbeo.com/common/api.jsp
#
#PLEASE NOTE: In order to access this data an API Key is required. Free API Key can be requested for academic projects
#For details regarding the same refer the link given above
#
######################################################

import requests
from pandas.io.json import json_normalize

BASE_URL = "http://www.numbeo.com:8008/api/"
COUNTRY = "United States"

def api_quality_life(NUMBEO_API_KEY=None, out_filename=None):
    '''
    Function to fetch the quality of life index data from the Numbeo Website using their API
    *** API Key is required to run this function and can be obtained from NUMBEO WEBSITE***
    
    Arguments:
        NUMBEO_API_KEY (str):
            API Key needed to access the NUMBEO Website Data using its API
            
        out_filename (str):
            CSV Filename to store the data collected using the NUMBEO API
            Make sure to include the complete path in the filename
    
    Returns:
        CSV File at the location specified by the filename path
        It contains the quality of life index for prominent cities in United States
        Additionally, it will also contain other indexes such as cost of living, crime rate etc that will be removed in processing later
    
    Our Filename: "../../raw_data/quality_of_life_cities.csv"
    '''
    
    assert isinstance(NUMBEO_API_KEY, str), 'Input API Key is not a string'
    assert isinstance(out_filename, str), 'Input filename is not a string'
    
    SECTION='12' #Section corresponding to quality of life 
    parameters = {'api_key':NUMBEO_API_KEY,'section':SECTION} #Parameters needed in API request
    response = requests.get(BASE_URL+"/rankings_by_city_current",params=parameters) #Request the index information using API
    
    requested_data_json = response.json()
    try:
        requested_data_json['error'] #Check whether the response has returned an error
        print('Error Response from API')
        print(requested_data_json['error']) #If error is present, return the error and exit from the function
        assert False, 'Refer printed error'
    except:
        pass #if no error - do nothing
    
    qol_df = json_normalize(requested_data_json) #JSON Data obtained from response converted to dataframe
    qol_US_df = qol_df[qol_df.country == COUNTRY] #Retain entries of United States Only
    qol_US_df.to_csv(out_filename) #Export data as csv to given filename