#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script contains the general function definitions required throughout the project
#
######################################################

import pandas as pd
import geocoder

def get_city_US_list(in_filename=None):
    '''
    This function gives the list of all cities in the format - city, state, United States
    These are the final cities being analyzed throughout the project - the ones that have all 55 item/component price entries
    
    Arguments:
        in_filename (str):
            The input file that contains the cleaned dataset of all item/component prices for cities
            Make sure that the filename contains the entire path
            
    Returns:
        (list):
            Final list of all cities containing 55 entries
    '''
    
    assert isinstance(in_filename, str), 'Input filename is not a string'
    
    city_df = pd.read_csv(in_filename)
    city_US_list = city_df['name'].unique().tolist() #Find unique cities in the dataframe and convert to string
    city_US_list = [each.replace(', United States','') for each in city_US_list]
    
    return city_US_list

def state_full(state_abr=None):
    '''
    This function gives the complete state name from the two letter abbreviation of the state
    
    Arguments:
        state_abr (str):
            Two letter abbreviation of the state
    
    Returns:
        (str):
            Complete state name
    '''
    
    assert isinstance(state_abr, str), 'Input state abbreviation is not a string'
    assert len(state_abr) is 2, 'Input is not a two letter abbreviation'
    assert state_abr.isalpha(), 'Input is not a string of alphabets'
    assert state_abr.isupper(), 'Input is not all capital letters'
    
    states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'}
    
    state_full = states[state_abr]
    return state_full

def get_county(GOOGLE_API_KEY=None, city=None, state_abr=None):
    '''
    Function returns the county information for the given city, state
    
    Arguments:
        GOOGLE_API_KEY (str):
            API Key to access Google's geolocation information
        city (str):
            City for which county information is to be found
        state_abr (str):
            Two alphabet abbreviation of the state 
            
    Returns:
        (str):
            Name of the county
    '''
    
    assert isinstance(GOOGLE_API_KEY, str), 'API Key must be a string'
    assert isinstance(city, str), 'Input city is not a string'
    assert isinstance(state_abr, str), 'Input state is not a string'
    assert len(state_abr) is 2, 'Input state is not a two letter abbreviation'
    
    city_state = city + ', ' + state_abr
    
    result = geocoder.google(city_state, key=GOOGLE_API_KEY) #Get location information from Google API
    return result.current_result.county #return extracted county information

def strip_dollar_comma(x):
    '''
    Remove the dollar and comma price information in the dataset
    
    Arguments:
        x (str or pandas Series):
            Input price string or series from which the dollar and comma is to be removed
    
    Returns:
        (float/s):
            Returns a series of floats or single float value based on the input
    '''
    if isinstance(x,str):
        x=x.strip('$')
        x=x.replace(',','')
        x=float(x)
    else:    
        x=x.str.strip('$')
        x=x.str.replace(',','')
        x=x.astype(float)
    
    return x