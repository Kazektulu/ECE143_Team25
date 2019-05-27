from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import csv
from api_counties import *
import pandas as pd

filename = 'Numbeo_API_Data/county.csv'

def salary_scraper(url):
    '''
    
    '''
    
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(1)
    
    main_page = browser.current_window_handle
    health_dict = {}
    state_county_df = county_state_df(filename)
    with open('Numbeo_API_Data/salary.csv','w+',newline='') as fp:
        csv_writer = csv.writer(fp)
        for i in range(len(state_county_df)):
#        for i in range(2):
            state_link = browser.find_element_by_partial_link_text(state_county_df['state'][i])
            state_link.send_keys(Keys.CONTROL,Keys.RETURN)
            for window in browser.window_handles:
                if(window != main_page):
                    state_page = window
            browser.switch_to.window(state_page)
        
            time.sleep(1)
            county_link = browser.find_element_by_partial_link_text(state_county_df['County'][i])
            county_link.click()
        
            soup = BeautifulSoup(browser.page_source, 'html.parser')
        
            salary_dict={}
        
            salary_table = soup.find('table', attrs={'summary':'Typical annual salaries'})
            salary_table_rows = salary_table.findAll('tr')
            for row in salary_table_rows:
                salary_table_cols = row.findAll('td')
                if len(salary_table_cols) is 2:
                    salary_dict[f"{salary_table_cols[0].find(text=True).strip()}"] = salary_table_cols[1].find(text=True).strip()
                    
            expenses_table = soup.find('table', attrs={'summary':'Typical family expenses for various family sizes.'})
            expenses_table_rows = expenses_table.findAll('tr')
            for row in expenses_table_rows:
                expenses_table_cols = row.findAll('td')
                if len(expenses_table_cols) is not 0:
                    if (str(expenses_table_cols[0].find(text=True).strip()) == 'Medical'):
                        health_dict[f"{state_county_df['City_state'][i]}"] = expenses_table_cols[1].find(text=True).strip()
                        
            if i is 0:
                csv_writer.writerow(list(salary_dict.keys()))
            csv_writer.writerow(list(salary_dict.values()))
            
            browser.close()
            browser.switch_to.window(main_page)
            time.sleep(1)
            
    browser.close()
    health_df = pd.DataFrame.from_dict(health_dict,orient='index')
    health_df.to_csv('Numbeo_API_Data/health.csv')
#    return health_dict
#    return salary_dict
    
url = 'http://livingwage.mit.edu/'
salary_scraper(url)    