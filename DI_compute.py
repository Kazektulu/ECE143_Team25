import pandas as pd
from api_counties import *

def di_compute(salary, city, state):
    '''
    
    '''
    
    fed_tax = fed_tax_compute(salary)
    state_tax = state_tax_compute(salary, state)
    CoL = CoL_compute(city, state)
    DI = salary - fed_tax - state_tax - CoL
    
    return DI, CoL, state_tax, fed_tax
    
def CoL_compute(city, state):
    '''
    
    '''
    
    col_path = 'Numbeo_API_Data/CoL_Salary.csv'
    col_df = pd.read_csv(col_path, encoding = 'iso-8859-1')
    CoL = col_df[(col_df.city == city) & (col_df.state == state)]['CoL Per Year'].values[0]
#    CoL = pd.to_numeric(CoL, errors='coerce').astype(float)
    return CoL
    
def fed_tax_compute(salary):
    '''
    
    '''
    
    fed_tax_path = 'tax_Data/fed.csv'
    fed_tax_df = pd.read_csv(fed_tax_path, encoding = 'iso-8859-1')
    fed_tax_df.drop(columns=['family_threshold'], inplace=True)
    fed_tax_df.set_index('single_threshold',inplace=True)
    fed_dict = fed_tax_df.to_dict()['single_rate']
    fed_key_list = list(fed_dict.keys())
    fed_rate_index = max([each for each in fed_key_list if each < salary])
    fed_rate = int(fed_dict[fed_rate_index].strip('%'))/100
    fed_tax = salary * fed_rate
    
    return fed_tax

def state_tax_compute(salary, state):
    '''
    
    '''
    
    state_tax_path = 'tax_Data/2019_tax.csv'
    state_tax_df = pd.read_csv(state_tax_path, encoding = 'iso-8859-1')
    state_tax_df.drop(columns=['family_threshold','family_rate'], inplace=True)
    
    state_tax_groups = state_tax_df.groupby('state')
    state_tax_dict = {}
    for name, group in state_tax_groups:
        state_tax_dict[f"{name}"] = group
    
    state_tax_current_df = state_tax_dict[state]
    temp_df = state_tax_current_df.drop(columns=['state'])
    temp_df['single_threshold'] = temp_df['single_threshold'].apply(lambda x: strip_dollar_comma(x))
    temp_df.set_index('single_threshold', inplace=True)
    state_dict = temp_df.to_dict()['single_rate']
    
    state_key_list = list(state_dict.keys())
    state_rate_index = max([each for each in state_key_list if each < salary])
    state_rate = float(state_dict[state_rate_index].strip('%'))/100
    state_tax = salary * state_rate
    
    return state_tax
    
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

salary_samples_path = 'Numbeo_API_Data/Salary_Samples.csv'
salary_samples = pd.read_csv(salary_samples_path, encoding = 'iso-8859-1')
DI_list = []
CoL_list = []
state_tax_list = []
fed_tax_list = []
complete_dict = {}

for index,each in salary_samples.iterrows():
    DI, CoL, State_Tax, Federal_Tax = di_compute(each.Salary, each.City, each.State)
    DI_list.append(DI)
    CoL_list.append(CoL)
    state_tax_list.append(State_Tax)
    fed_tax_list.append(Federal_Tax)

complete_dict['DI'] = DI_list
complete_dict['CoL'] = CoL_list
complete_dict['State_Tax'] = state_tax_list
complete_dict['Federal_Tax'] = fed_tax_list
DI_df = pd.DataFrame.from_dict(complete_dict)
salary_samples_update = pd.concat([salary_samples, DI_df], axis=1)

salary_samples_update.to_csv('Numbeo_API_Data/Salary_samples_updated.csv')
