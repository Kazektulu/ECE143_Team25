#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script includes the functions needed to compute the discretionary income and individual components for a set of chosen job prospects
#Job descriptions were manually obtained from Glassdoor: https://www.glassdoor.com/index.htm
#General Field Area - Data Science Jobs
#
######################################################
import pandas as pd

from discretionary_income_compute import compute_discretionary_income

def sample_job_processor(job_sample_filename):
    '''
    This function computes the discretionary income and the individual components for each of the sample job salaries in the input file
    
    Arguments:
        job_sample_filename (str):
            Input file containing the descriptions of the sample jobs being considered
        
    Returns:
        (pandas DataFrame):
            Dataframe containing the computed discretionary income and cost of living, tax components
    '''
    
    assert isinstance(job_sample_filename, str), 'Input filename is not a string'
    
    job_samples = pd.read_csv(job_sample_filename, encoding = 'iso-8859-1')
    
    DI_list = []
    CoL_list = []
    state_tax_list = []
    fed_tax_list = []
    complete_dict = {}
    
    price_filename = '../../raw_data/clean_city_item_prices.csv'
    health_filename = '../../raw_data/health_data.csv'
    fed_tax_filename = '../../raw_data/federal_tax_manual.csv'
    state_tax_filename = '../../raw_data/state_tax_manual.csv'
    
    for index,each in job_samples.iterrows(): #for each of the job samples compute the individual components
        DI, CoL, State_Tax, Federal_Tax = compute_discretionary_income(each.Salary, each.State, each.City, price_filename, health_filename, fed_tax_filename, state_tax_filename)
        DI_list.append(DI)
        CoL_list.append(CoL)
        state_tax_list.append(State_Tax)
        fed_tax_list.append(Federal_Tax)
        
    complete_dict['DI'] = DI_list
    complete_dict['CoL'] = CoL_list
    complete_dict['State_Tax'] = state_tax_list
    complete_dict['Federal_Tax'] = fed_tax_list
    DI_df = pd.DataFrame.from_dict(complete_dict) #create final dataframe with all of the components and the final discretionary income
    job_samples_update = pd.concat([job_samples, DI_df], axis=1) #return updated dataframe with all of the computed values
    
    return job_samples_update

if __name__ == "__main__":
    
    job_sample_filename = '../../raw_data/job_samples_manual.csv'
    job_df = sample_job_processor(job_sample_filename)
    job_df.to_csv('../../processed_data/job_samples_di_components.csv')