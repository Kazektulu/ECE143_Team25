#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script includes the functions needed to compute the final discretionary income after all the components have been evaluated
#
######################################################

import pandas as pd

from income_components_compute import compute_federal_tax, compute_state_tax, compute_cost_of_living, compute_all_cost_of_living
from income_components_compute import compute_federal_tax_df, compute_state_tax_df
from utils import strip_dollar_comma

def compute_discretionary_income(salary, state, city, price_filename, health_filename, fed_tax_filename, state_tax_filename):
    '''
    Function to compute the discretionary income for a given salary and location
    
    Arguments:
        salary (float or int):
            Salary for which the discretionary income is to be computed
        state (str):
            Name of the state - COMPLETE NAME
        city (str):
            Name of the city
        price_filename (str):
            CSV FILE - Path of file that contains the inidividual item prices for all cities
        health_filename (str):
            CSV FILE - Path of file that contains the health expense for all cities
        fed_tax_filename (str):
            CSV FILE - Path of file that contains the federal tax rates
        state_tax_filename (str):
            CSV FILE - Path of file that contains the state tax rates
            
    Returns:
        1-(float):
            Computed discretionary income value
        2-(float):
            Corresponding cost of living
        3-(float):
            Computed state tax
        4-(float):
            Computed federal tax
    '''
    
    assert isinstance(salary, (int,float)), 'Input salary is not an int or float'
    assert isinstance(state, str), 'Input state is not a string'
    assert isinstance(city, str), 'Input city is not a string'
    assert isinstance(price_filename, str), 'Input price filename is not a string'
    assert isinstance(health_filename, str), 'Input health filename is not a string'
    
    fed_tax = compute_federal_tax(fed_tax_filename,salary) #compute federal tax
    state_tax = compute_state_tax(state_tax_filename, salary, state) #compute state tax
    CoL = compute_cost_of_living(city, state, price_filename, health_filename) #compute cost of living
    DI = salary - fed_tax - state_tax - CoL #compute discretionary income from all of the above components
    
    return DI, CoL, state_tax, fed_tax

def compute_all_discretionary_income(price_filename, health_filename, salary_filename, fed_tax_filename, state_tax_filename):
    '''
    Function to compute the discretionary income for all the cities in our original Numbeo database
    
    Arguments:
        price_filename (str):
            CSV FILE - Path of file that contains the inidividual item prices for all cities
        health_filename (str):
            CSV FILE - Path of file that contains the health expense for all cities
        salary_filename (str):
            CSV FILE - Path of file that contains the average salary for all cities for different occupations
        fed_tax_filename (str):
            CSV FILE - Path of file that contains the federal tax rates
        state_tax_filename (str):
            CSV FILE - Path of file that contains the state tax rates
            
    Returns:
        (pandas DataFrame):
            Containing the computed discretionary income for all the cities  
    '''
    
    assert isinstance(price_filename, str), 'Input price filename is not a string'
    assert isinstance(health_filename, str), 'Input health filename is not a string'
    assert isinstance(salary_filename, str), 'Input salary filename is not a string'
    
    col_df = compute_all_cost_of_living(price_filename, health_filename) #read the cost of living
    
    salary_df = pd.read_csv(salary_filename, index_col=0) #read the salary data
    salary_df = salary_df.apply(lambda x: strip_dollar_comma(x), axis=1)
    
    fed_tax_df = compute_federal_tax_df(fed_tax_filename, salary_df.astype(float)) #compute federal tax
    state_tax_df = compute_state_tax_df(state_tax_filename, salary_df.astype(float)) #compute state tax
    
    salary_after_tax_df = salary_df.astype(float) - fed_tax_df.astype(float) - state_tax_df.astype(float) #compute disposable income remaining after the tax has been deducted
    
    discretionary_income_df = pd.DataFrame(index=salary_after_tax_df.index, columns = salary_after_tax_df.columns)
    for column in salary_after_tax_df.columns:
        discretionary_income_df[column] = salary_after_tax_df[column] - col_df['CoL Per Year'] #subtract the cost of living to compute discretionary income
    
    discretionary_income_final_df = pd.concat([discretionary_income_df,col_df],axis=1) #append cost of living to discretionary income for final dataframe
    
    return discretionary_income_final_df
    
if __name__ == "__main__":
    
    price_filename = '../../raw_data/clean_city_item_prices.csv'
    health_filename = '../../raw_data/health_data.csv'
    salary_filename = '../../raw_data/salary_data.csv'
    fed_tax_filename = '../../raw_data/federal_tax_manual.csv'
    state_tax_filename = '../../raw_data/state_tax_manual.csv'
    
    final_di=compute_all_discretionary_income(price_filename, health_filename, salary_filename, fed_tax_filename, state_tax_filename)
    final_di.to_csv('../../processed_data/discretionary_income_col.csv')