import requests
import json
import pandas as pd

BASE_URL = "http://www.numbeo.com:8008/api/"
API_KEY = "i3yomanspm7o3r"
COUNTRY = "United States"

# Trinity's north carolina problem - not happening before - solve before final submit
# For now - name changed in the cities.csv

def cities_API():
    '''
    Collect names of all cities in the Numbeo database
    Omits cities for which there is no data
    Returns:
        Json/Csv file
    '''
#    Request data using API
    parameters = {'api_key':API_KEY}
    response = requests.get(BASE_URL+"/cities",params=parameters)
    
#    Write data to a json file
    with open('cities.json','w') as fp:
        json.dump(response.json(),fp)
        
#    Convert from json to csv file for better readibility
#    json_to_csv('cities.json','cities.csv')
        
def country_prices(country):
    '''
    Collect current prices for a particular country
    Args:
        country (str): The name of the country 
    Returns:
        Json/Csv file
    '''
#    Request data using API
    parameters = {'api_key':API_KEY, 'country':country}
    response = requests.get(BASE_URL+"/country_prices",params=parameters)

#    Write data to a json file
    with open(f"country_prices_{country}.json",'w') as fp:
        json.dump(response.json(),fp)
        
#    Convert from json to csv file for better readibility
#    json_to_csv(f"country_prices_{country}.json", f"country_prices_{country}.csv")

def city_price():
    '''
    Collect current prices for a particular country
    Args:
        country (str): The name of the country 
    Returns:
        Json/Csv file
    '''
    
#    Request data using API
    data = pd.read_csv('Numbeo_API_Data/cities.csv' , encoding = 'iso-8859-1')
    data_US = data[data.country == 'United States']
    cities_US_list = data_US.city.tolist()
#    cities_US_list.remove("trinity's north carolina")
    
    for index,city in enumerate(cities_US_list):
        parameters = {'api_key':API_KEY, 'country':COUNTRY, 'city':city}
        response = requests.get(BASE_URL+"/city_prices",params=parameters)
        
        data=response.json()
        try:
            data['error']
            continue
        except:
            pass
        
        df=pd.DataFrame(data)
        df = pd.concat([df.drop(['prices'],axis=1),df['prices'].apply(pd.Series)],axis=1)
        df.to_csv(f"Numbeo_API_Data/city_prices_final/{index}_prices.csv")
#        
#        
#        with open(f"City_json_final/{index}_prices.json",'w') as fp:
#            json.dump(response.json(),fp)
#    
#    Convert json files to csv files using pandas
#    for index,city in enumerate(cities_US_list):
#        print(city)
#        
##        df = pd.read_json(f"City_json_final/{index}_prices.json")
#        df = pd.concat([df.drop(['prices'],axis=1),df['prices'].apply(pd.Series)],axis=1)
#        df.to_csv(f"Numbeo_API_Data/city_prices_final/{index}_prices.csv")
#    return cities_US_list
    
def json_to_csv(inputfile, outputfile):
    '''
    Convert input json file to csv file
    '''
    
    assert isinstance(inputfile, str), 'Input filename is not a string'
    assert isinstance(outputfile, str), 'Output filename is not a string'
    
    df = pd.read_json(inputfile)
    df = pd.concat([df.drop([df.columns[-1]],axis=1),df[df.columns[-1]].apply(pd.Series)],axis=1)
    df.to_csv(outputfile)
    
# Collect names of all cities in United States from cities data
#data = pd.read_csv('Numbeo_API_Data/cities.csv')
#data_US = data[data.country == 'United States']
#cities_US_list = data_US.city.tolist()

#for city in cities_US_list:
#    city_price(city)
    
def get_county():
    '''
    
    '''
    
    locations = ['Chicago, IL', 'San Francisco, CA']

    city_data_url = 'http://api.sba.gov/geodata/primary_links_for_city_of/%s/%s.json'
    
    for l in locations:
        split_name = l.split(', ')
        response = requests.get(city_data_url % tuple(split_name))
    
        resp_json = json.loads(response.text)
        print(resp_json[0]['full_county_name'])
        
#parameters = {'api_key':API_KEY, 'country':COUNTRY, 'city':Aberdeen}
#response = requests.get(BASE_URL+"/city_prices",params=parameters)
        
def QoL_api():
    '''
    
    '''
    
    SECTION='12'
    parameters = {'api_key':API_KEY,'section':SECTION}
    response = requests.get(BASE_URL+"/rankings_by_city_current",params=parameters)
    
    with open('qol_cities.json','w') as fp:
        json.dump(response.json(),fp)
        
    qol_df = pd.read_json("qol_cities.json")
    qol_US_df = qol_df[qol_df.country == 'United States']
    qol_US_df.to_csv('Numbeo_API_Data/qol_cities.csv')