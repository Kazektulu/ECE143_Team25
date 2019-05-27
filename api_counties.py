import geocoder
import pandas as pd

API_KEY = 'AIzaSyAV3tjMoAOeUHUA0opCQciAzi6EdKGgwvc'

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

def get_county():
    
    county_dict={}
    with open('Numbeo_API_Data/final_city_state.txt','r') as f:
        city_state_US_list = f.read().split('\n')
    
    for each in city_state_US_list:
        result = geocoder.google(each, key=API_KEY)
        county_dict[f"{each}"] = result.current_result.county
        
#    county_df = pd.DataFrame(county_dict, columns = ['county'])
    county_df = pd.DataFrame.from_dict(county_dict,orient='index')
    county_df.to_csv('Numbeo_API_Data/county.csv') 
    return

def county_state_df(filename, state_map=states):
    '''
    
    '''
    
    county_df = pd.read_csv(filename)
    county_df.rename(columns = {'Unnamed: 0': 'City_state', '0':'County'}, inplace=True)
    county_df['city'], county_df['state'] = county_df['City_state'].str.split(pat=', ').str
    county_df['state'] = county_df['state'].map(states)
    
    return county_df
    
    
