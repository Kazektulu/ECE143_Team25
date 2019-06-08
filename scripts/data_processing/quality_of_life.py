#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script appends the quality of life index to create a final compiled dataframe
#As the quality of life index is not available for all of the entries, the missing data is simply set to zero and not included in the analysis
######################################################
import pandas as pd

def quality_of_life_append(di_filename, qol_filename, out_filename):
    '''
    Function to append the quality of life data to the processed final discretionary income dataset
    
    Arguments:
        di_filename (str):
            Input file that contains the processed discretionary income dataset
        qol_filename (str):
            Input file that contains the raw quality of life dataset
        out_filename (str):
            Path to store the final dataset including the quality of life index
    
    Returns:
        CSV File that contains the quality of life index alongwith the processed discretionary income
    '''
    
    assert isinstance(di_filename, str), 'Input di filename is not a string'
    assert isinstance(qol_filename, str), 'Input qol filename is not a string'
    assert isinstance(out_filename, str), 'Output filename is not a string'
    
    processed_di_df = pd.read_csv(di_filename, index_col=0)
    qol_df = pd.read_csv(qol_filename, index_col=2)
    
    final_df = pd.concat([processed_di_df, qol_df['quality_of_life_index']], axis=1) #concatenate the quality of life index to the computed discretionary income dataframe
    final_df.fillna(0, inplace=True) #replace all nans with zero
    final_df.to_csv(out_filename)