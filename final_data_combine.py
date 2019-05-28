import pandas as pd
from api_counties import *

def final_dataframe():
    '''
    
    '''
    
    Col_path = 'Numbeo_API_Data/CoL_final.csv'
    salary_path = 'Numbeo_API_Data/salary.csv'
    county_path = 'Numbeo_API_Data/county.csv'
    
    CoL_df = pd.read_csv(Col_path, index_col=1)
    Salary_df = pd.read_csv(salary_path, index_col=0)
    Salary_df = Salary_df.apply(lambda x: strip_dollar_comma(x), axis=1)
    
    county_df = county_state_df(county_path)
    county_df.drop(columns=['County'], inplace=True)
    county_df.set_index('City_state',inplace=True)
    
    CoL_Salary_df = pd.concat([county_df, CoL_df, Salary_df], axis=1)
    CoL_Salary_df.to_csv('Numbeo_API_Data/CoL_Salary.csv')
    
    Salary_after_fed_df = federal_tax_df(Salary_df)
    Salary_after_fed_df.to_csv('Numbeo_API_Data/Salary_After_Fed.csv')
    
    Salary_after_state_df = state_tax_df(Salary_df)
    Salary_after_state_df.to_csv('Numbeo_API_Data/Salary_After_State.csv')

def federal_tax_df(salary_df):
    '''
    
    '''
    
    salary_after_fed_df=pd.DataFrame(index=salary_df.index, columns=salary_df.columns)
    fed_tax_path = 'tax_Data/fed.csv'
    fed_tax_df = pd.read_csv(fed_tax_path)
    fed_tax_df.drop(columns=['family_threshold'], inplace=True)
    fed_tax_df.set_index('single_threshold',inplace=True)
    fed_dict = fed_tax_df.to_dict()['single_rate']
    for column in salary_df.columns:
        salary_after_fed_df[column] = salary_df[column].apply(lambda x: federal_tax_compute(x,fed_dict))
    return salary_after_fed_df

def federal_tax_compute(salary, fed_dict):
    '''
    
    '''
    
    fed_key_list = list(fed_dict.keys())
    fed_rate_index = max([each for each in fed_key_list if each < salary])
    fed_rate = int(fed_dict[fed_rate_index].strip('%'))/100
    salary = salary - salary*fed_rate
    return salary

def state_tax_df(salary_df):
    '''
    
    '''
    
#    salary_after_state_df=pd.DataFrame(index=salary_df.index, columns=salary_df.columns)
    state_tax_path = 'tax_Data/2019_tax.csv'
    state_tax_df = pd.read_csv(state_tax_path)
    state_tax_df.drop(columns=['family_threshold','family_rate'], inplace=True)
    
    state_tax_groups = state_tax_df.groupby('state')
    state_tax_dict = {}
    for name, group in state_tax_groups:
#        group.drop(columns=['state'], inplace=True)
#        group['single_threshold'] = group['single_threshold'].apply(lambda x: strip_dollar_comma(x))
#        group.set_index('single_threshold', inplace=True)
#        group_dict = group.to_dict()['single_rate']
        state_tax_dict[f"{name}"] = group
        
    for index,row in salary_df.iterrows():
        state_index = state_full(index)
        row = row.apply(lambda x: state_tax_compute(state_tax_dict[state_index],x))
        
    return salary_df

def state_tax_compute(state_tax_df, x):
    '''
    
    '''
    state_tax_df.drop(columns=['state'], inplace=True)
    state_tax_df['single_threshold'] = state_tax_df['single_threshold'].apply(lambda x: strip_dollar_comma(x))
    state_tax_df.set_index('single_threshold', inplace=True)
    state_dict = state_tax_df.to_dict()['single_rate']
    
    state_key_list = list(state_dict.keys())
    state_rate_index = max([each for each in state_key_list if each < x])
    state_rate = float(state_dict[state_rate_index].strip('%'))/100
    x = x - x*state_rate
    return x
    
    return

def strip_dollar_comma(x):
    '''
    
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
    