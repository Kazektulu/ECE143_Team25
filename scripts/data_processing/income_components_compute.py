#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script includes the functions needed to compute the components that will be utilized to evaluate discretionary income
#Components Include - Cost of Living, State Tax, Federal Tax
#
#The functions will work on the dataset obtained from the function under data collection and cleaning
#Make sure that you use the right filenames throughout
#
######################################################

import pandas as pd

from utils import get_city_US_list, strip_dollar_comma, state_full

def compute_cost_of_living(city, state, price_filename, health_filename):
    '''
    Computes the cost of living per year for a particular city and state 
    
    Arguments:
        city (str):
            Name of the city under consideration
        state (str):
            Name of the state under consideration - COMPLETE NAME
        price_filename (str):
            CSV FILE - Path of file that contains the inidividual item prices for all cities
        health_filename (str):
            CSV FILE - Path of file that contains the health expense for all cities
            
    Returns:
        (float):
            Computed cost of living value
    '''
    
    assert isinstance(city, str), 'Input city is not a string'
    assert isinstance(state, str), 'Input state is not a string'
    assert isinstance(price_filename, str), 'Input price filename is not a string'
    assert isinstance(health_filename, str), 'Input health filename is not a string'
    
    cost_of_living_df = compute_all_cost_of_living(price_filename, health_filename) #compute the cost of living for all entries
    cost_of_living_df.reset_index(inplace = True)
    cost_of_living_df[['city','state']] = cost_of_living_df['index'].str.split(", ",expand=True)
    cost_of_living_df['state'] = cost_of_living_df['state'].apply(lambda x:state_full(x)) #convert the state names to complete name to match nature of input
    
    CoL = cost_of_living_df[(cost_of_living_df.city == city) & (cost_of_living_df.state == state)]['CoL Per Year'].values[0] #return the cost of living for the particular city and state
    return CoL

def compute_all_cost_of_living(price_filename, health_filename):
    '''
    Computes the cost of living per year from the individual item prices and the health expense data obtained
    
    Arguments:
        price_filename (str):
            CSV FILE - Path of file that contains the inidividual item prices for all cities
        health_filename (str):
            CSV FILE - Path of file that contains the health expense for all cities
            
    Returns:
        (pandas DataFrame):
            Contains the final cost of living. Additionally it also contains an average leisure cost that considers movies, gym memberships and other non mandatory expenses
    '''
    
    assert isinstance(price_filename, str), 'Input price filename is not a string'
    assert isinstance(health_filename, str), 'Input health filename is not a string'
    
    original_df = pd.read_csv(price_filename)#This is the original dataframe
    original_df['city_state'] = original_df['name'].str.replace(', United States','')
    
    original_df_ngroups = original_df.groupby('city_state').ngroups
    
    city_list = get_city_US_list('../../raw_data/clean_city_item_prices.csv') #get the list of all cities

    assert (original_df_ngroups == len(city_list)), 'Input price file has inadequate entries'
    assert all(original_df.city_state.isin(city_list)), 'Entries in the input price file are inconsistent with the rest of the database'
    
    filtered_df = original_df.drop(['lowest_price','highest_price'],axis=1)# This is the data after deleting low and high price - we will only consider average price
    filtered_df = filtered_df.fillna(0)
       
    CoL={}#This is the dictionary that contains the cost of living of final 302 cities in the US
    Leisure={}#This will contain the cost associated with leisure per year
    
    #Compute the cost of living and leisure expenditure from the 55 items in the dataframe for each city
    #Utilized our own metric for estimating the CoL - Can be found in the Read Me
    for i in range(len(city_list)):
        CoL[city_list[i]]=filtered_df.iat[(21+i*55),9]*12+filtered_df.iat[(25+i*55),9]*12+filtered_df.iat[(27+i*55),9]*12+(55*12)+filtered_df.iat[(18+i*55),9]*12+filtered_df.iat[(19+i*55),9]*1892+filtered_df.iat[(0+i*55),9]*156+filtered_df.iat[(2+i*55),9]*208+filtered_df.iat[(1+i*55),9]*26+filtered_df.iat[(9+i*55),9]*25+filtered_df.iat[(7+i*55),9]*52+filtered_df.iat[(8+i*55),9]*78+filtered_df.iat[(17+i*55),9]*13+filtered_df.iat[(49+i*55),9]*250+filtered_df.iat[(45+i*55),9]*26+filtered_df.iat[(46+i*55),9]*26+filtered_df.iat[(47+i*55),9]*13+filtered_df.iat[(48+i*55),9]*52+filtered_df.iat[(50+i*55),9]*7+filtered_df.iat[(51+i*55),9]*26+filtered_df.iat[(52+i*55),9]*52+filtered_df.iat[(53+i*55),9]*26+filtered_df.iat[(54+i*55),9]*13+filtered_df.iat[(33+i*55),9]+filtered_df.iat[(31+i*55),9]*2+filtered_df.iat[(32+i*55),9]*2+filtered_df.iat[(34+i*55),9]                                                                                                                 
        Leisure[city_list[i]]=filtered_df.iat[(28+i*55),9]*12+filtered_df.iat[(30+i*55),9]*5
        
    #Create new dataframes from the cost of living and leisure information
    CoL_df=pd.DataFrame(pd.Series(CoL),columns=['CoL Per Year'])
    CoL_df['Leisure'] = pd.Series(Leisure)
    
    health_df = pd.read_csv(health_filename, encoding = 'iso-8859-1') #read the health expense data
    
    assert (len(health_df) == len(city_list)), 'Input health information has inadequate entries'
    assert all(health_df.City_state.isin(city_list)), 'Entries in the input health file are inconsistent with the rest of the database'
    
    health_df['Health'] =health_df['Health'].apply(lambda x:x[1:2]+x[3:]).astype(int) #remove the dollar sign and the comma in the information and convert information to int type
    health_df = health_df.set_index('City_state')
    CoL_df['Health'] = health_df['Health'] #append the health values to the cost of living dataframe
    CoL_df['CoL Per Year'] = CoL_df['CoL Per Year'] + CoL_df['Health'].astype(int) #add the health expenditure to the cost of living computed earlier
    
    return CoL_df

def compute_federal_tax(fed_tax_filename, salary):
    '''
    Function to compute the federal tax amount for the input salary
    
    Arguments:
        fed_tax_filename (str):
            Filename (Complete Path) that includes federal tax rates and threshold
        salary (int/float):
            Salary amount in USD for which tax is to be computed
            
    Returns:
        (float):
            Amount of federal tax to be applied
    '''
    
    assert isinstance(fed_tax_filename, str), 'Input filename is not a string'
    assert isinstance(salary, (int,float)), 'Input salary is not an int or float'
    assert salary >= 0, 'Input salary is not positive'
    
    fed_tax_df = pd.read_csv(fed_tax_filename, encoding = 'iso-8859-1') #read the federal tax rates and the corresponding thresholds
    fed_tax_df.drop(columns=['family_threshold'], inplace=True) #family level analysis is not being done
    fed_tax_df.set_index('single_threshold',inplace=True)
    fed_dict = fed_tax_df.to_dict()['single_rate'] #create dictionary to map thresholds to rate
    fed_key_list = list(fed_dict.keys())
    fed_rate_index = max([each for each in fed_key_list if each < salary]) #find the rate applicable for the given input salary
    fed_rate = int(fed_dict[fed_rate_index].strip('%'))/100 #remove the unwanted characters in tax rate and convert to int 
    fed_tax = salary * fed_rate
    
    return fed_tax

def compute_federal_tax_df(fed_tax_filename, salary_df):
    '''
    Function to compute the federal tax amount for the input salary dataframe
    
    Arguments:
        fed_tax_filename (str):
            Filename (Complete Path) that includes federal tax rates and threshold
        salary df (pandas Dataframe):
            Salary dataframe with amount in USD for which tax is to be computed
            
    Returns:
        (pandas Dataframae):
            Amount of federal tax to be applied for all entries
    '''
    
    assert isinstance(fed_tax_filename, str), 'Input filename is not a string'
    assert isinstance(salary_df, pd.DataFrame), 'Input salary is not a pandas Dataframe'
    
    salary_fed_tax_df=pd.DataFrame(index=salary_df.index, columns=salary_df.columns)
    for column in salary_df.columns:
        salary_fed_tax_df[column] = salary_df[column].apply(lambda x: compute_federal_tax(fed_tax_filename, x)) #apply federal tax computation on each of the columns in salary dataframe
    return salary_fed_tax_df

def compute_state_tax(state_tax_filename, salary, state):
    '''
    Function to compute the state tax amount for the input salary
    
    Arguments:
        fed_tax_filename (str):
            Filename (Complete Path) that includes state wise tax rates and threshold
        salary (float or int):
            Salary amount in USD for which tax is to be computed
        state (str):
            Name of state under consideration - COMPLETE NAME
            
    Returns:
        (float):
            Amount of state tax to be applied
    '''
    
    assert isinstance(state_tax_filename, str), 'Input filename is not a string'
    assert isinstance(salary, (int,float)), 'Input salary is not an int or float'
    assert salary >= 0, 'Input salary is not positive'
    assert isinstance(state, str), 'Input state is not a string'
    
    state_tax_df = pd.read_csv(state_tax_filename, encoding = 'iso-8859-1')
    state_tax_df.drop(columns=['family_threshold','family_rate'], inplace=True)
    
    state_tax_groups = state_tax_df.groupby('state') #group the tax rates and threshold by the state
    state_tax_dict = {}
    for name, group in state_tax_groups:
        state_tax_dict[f"{name}"] = group #create dictionary of dataframes where each entry corresponds to a state
    
    state_tax_current_df = state_tax_dict[state]
    temp_df = state_tax_current_df.drop(columns=['state'])
    temp_df['single_threshold'] = temp_df['single_threshold'].apply(lambda x: strip_dollar_comma(x)) #remove the dollar and commas from price data
    temp_df.set_index('single_threshold', inplace=True)
    state_dict = temp_df.to_dict()['single_rate'] #create dictionary to map thresholds to rate
    
    state_key_list = list(state_dict.keys())
    state_rate_index = max([each for each in state_key_list if each < salary]) #find the applicable tax rate
    state_rate = float(state_dict[state_rate_index].strip('%'))/100
    state_tax = salary * state_rate #compute the amount of tax applicable
    
    return state_tax

def compute_state_tax_df(state_tax_filename, salary_df):
    '''
    Function to compute the state tax amount for the input salary dataframe
    
    Arguments:
        fed_tax_filename (str):
            Filename (Complete Path) that includes state wise tax rates and threshold
        salary (pandas DataFrame):
            Salary dataframe with amount in USD for which tax is to be computed
            
    Returns:
        (pandas DataFrame):
            Amount of state tax to be applied
    '''
    
    assert isinstance(state_tax_filename, str), 'Input filename is not a string'
    assert isinstance(salary_df, pd.DataFrame), 'Input salary is not a pandas Dataframe'
    
    state_tax_list = []    
    for index,row in salary_df.iterrows():
        city, state = index.split(', ')
        state_index = state_full(state)
        p = row.apply(lambda x: compute_state_tax(state_tax_filename,x,state_index)) #send each row to the compute function to evaluate the 
        p = p.to_frame()
        state_tax_list.append(p.T) #create list of transformed rows containing the tax information
    salary_state_tax_df = pd.concat(state_tax_list)
    
    return salary_state_tax_df
    
if __name__ == "__main__":
    
    price_filename = '../../raw_data/clean_city_item_prices.csv'
    health_filename = '../../raw_data/health_data.csv'
    salary_filename = '../../raw_data/salary_data.csv'
    final_col_df = compute_all_cost_of_living(price_filename, health_filename)
    