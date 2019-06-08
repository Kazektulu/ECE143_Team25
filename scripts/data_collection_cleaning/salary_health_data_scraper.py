#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script includes the functions needed to collect the health expenditure component of cost of living and the average salary over counties
#Details of the Website - http://livingwage.mit.edu/
#
#Data on this website is sorted based on counties and county information is missing in the Numbeo dataset
#County information can be obtained using the GOOGLE Geocoding API: https://developers.google.com/maps/documentation/geocoding/start
#
#PLEASE NOTE: In order to access the county data using Google API - API Key is required
#
######################################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd

from utils import get_city_US_list, state_full, get_county

url = 'http://livingwage.mit.edu/'

def salary_scraper(out_filename=None, GOOGLE_API_KEY=None):
    '''
    Function to scrape county wise average salary data for all occupations on the website
    
    Arguments:
        out_filename (str):
            CSV Filename to store the salary data
            Make sure to include the complete file path
            
    Returns:
        CSV File that contains the average salary for different set of occupations
        
    Our Filename: "../../raw_data/salary_data.csv"
    '''
    
    assert isinstance(out_filename, str), 'Input filename is not a string'
    assert isinstance(GOOGLE_API_KEY, str), 'Input API KEY is not a string'
    
    browser = webdriver.Chrome() #open the chrome browser
    browser.get(url) #open the website 
    time.sleep(1) #time delay to let the page load completely
    
    main_page = browser.current_window_handle #store main page handle to return to later
    
    city_list = get_city_US_list('../../raw_data/clean_city_item_prices.csv') #get the list of all cities
    county_dict = {}
    
    for each in city_list:
        city, state, country = each.split(', ')
        city_state = city + ', ' + state
        county_dict[city_state] = get_county(GOOGLE_API_KEY, city, state)
    
    with open(out_filename,'w+',newline='') as fp:
        csv_writer = csv.writer(fp)
        for key in county_dict.keys():
            city,state = key.split(', ')
            state_link = browser.find_element_by_partial_link_text(state_full(state)) #find the link for the state
            state_link.send_keys(Keys.CONTROL,Keys.RETURN) #ctr+enter to click on link
            for window in browser.window_handles:
                if(window != main_page):
                    state_page = window
            browser.switch_to.window(state_page) #open the link in a new tab for easier navigation to main window later
        
            time.sleep(1) #time delay to let the page load completely
            county_link = browser.find_element_by_partial_link_text(county_dict[key]) #find the link for the county
            county_link.click() #click on the link
        
            soup = BeautifulSoup(browser.page_source, 'html.parser') 
        
            salary_dict={}
        
            salary_table = soup.find('table', attrs={'summary':'Typical annual salaries'}) #extract the average salary values from the webpage table
            salary_table_rows = salary_table.findAll('tr')
            for row in salary_table_rows:
                salary_table_cols = row.findAll('td')
                if len(salary_table_cols) is 2:
                    salary_dict[f"{salary_table_cols[0].find(text=True).strip()}"] = salary_table_cols[1].find(text=True).strip() #append the scraped salary information to the dictionary
                      
            if each is city_list[0]:
                csv_writer.writerow(list(salary_dict.keys())) #when writing the first entry, first write the header
            csv_writer.writerow(list(salary_dict.values()))
            
            browser.close() #close the opened new tab
            browser.switch_to.window(main_page) #switch to the main page with links to all states
            time.sleep(1)
            
    browser.close() #close the main page and exit chrome browser
    return

def health_data_scraper(out_filename=None, GOOGLE_API_KEY=None):
    '''
    Function to scrape county wise average health expenditure for cost of living estimation
    
    Arguments:
        out_filename (str):
            CSV Filename to store the health data
            Make sure to include the complete file path
            
    Returns:
        CSV File that contains the health expenditure
        
    Our Filename: "../../raw_data/health_data.csv"
    '''
    
    assert isinstance(out_filename, str), 'Input filename is not a string'
    assert isinstance(GOOGLE_API_KEY, str), 'Input API KEY is not a string'
    
    browser = webdriver.Chrome() #open the chrome browser
    browser.get(url) #open the website 
    time.sleep(1) #time delay to let the page load completely
    
    main_page = browser.current_window_handle #store main page handle to return to later
    
    city_list = get_city_US_list('../../raw_data/clean_city_item_prices.csv') #get the list of all cities
    county_dict = {}
    
    for each in city_list:
        city, state = each.split(', ')
        city_state = city + ', ' + state
        county_dict[city_state] = get_county(GOOGLE_API_KEY, city, state)
    
    for key in county_dict.keys():
            state_link = browser.find_element_by_partial_link_text(state_full(state)) #find the link for the particular state
            state_link.send_keys(Keys.CONTROL,Keys.RETURN) #ctrl+enter to open link in new tab
            for window in browser.window_handles:
                if(window != main_page):
                    state_page = window
            browser.switch_to.window(state_page) #open window in new tab
        
            time.sleep(1)
            county_link = browser.find_element_by_partial_link_text(county_dict[key]) #find link for the county
            county_link.click() #click on the link
        
            soup = BeautifulSoup(browser.page_source, 'html.parser')
        
            health_dict={}

            expenses_table = soup.find('table', attrs={'summary':'Typical family expenses for various family sizes.'})
            expenses_table_rows = expenses_table.findAll('tr') #find health data in the expense table
            for row in expenses_table_rows:
                expenses_table_cols = row.findAll('td')
                if len(expenses_table_cols) is not 0:
                    if (str(expenses_table_cols[0].find(text=True).strip()) == 'Medical'):
                        health_dict[f"{key}"] = expenses_table_cols[1].find(text=True).strip()
                        
            browser.close() #close the opened new tab
            browser.switch_to.window(main_page) #shift to the main page
            time.sleep(1)
            
    browser.close() #close the main page and the chrome browser
    health_df = pd.DataFrame.from_dict(health_dict,orient='index')
    health_df.to_csv(out_filename)