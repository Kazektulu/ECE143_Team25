import pandas as pd
from api_counties import *
from final_data_combine import *
from sklearn import preprocessing

qol_path='Numbeo_API_Data/qol_cities.csv'
col_salary_path='Numbeo_API_Data/CoL_Salary.csv'
tax_path='Numbeo_API_Data/Salary_State.csv'
di_path='Numbeo_API_Data/Discretionary_Income_state.csv'

def qol_compile():
    '''
    
    '''
    
    qol_df = pd.read_csv(qol_path, index_col=2)
#    qol_df = city_state_separate(qol_df)
#    qol_df.set_index('city_name',inplace=True)
    qol_df=qol_df['quality_of_life_index']
    
    col_salary_df = pd.read_csv(col_salary_path, index_col=0)
    col_salary_df = pd.concat([col_salary_df['CoL Per Year'], col_salary_df['Computer & Mathematical']], axis=1)
    
    tax_df = pd.read_csv(tax_path, index_col=0)
    tax_df = tax_df['Computer & Mathematical'].rename('Tax')
    
    di_df = pd.read_csv(di_path, index_col=1)
    di_df = di_df['Computer & Mathematical'].rename('Discretionary Income')
    
    qol_compiled_df = pd.concat([qol_df, tax_df, col_salary_df, di_df], axis=1)
    qol_compiled_df.fillna(0, inplace=True)
    qol_compiled_df = qol_compiled_df[qol_compiled_df.quality_of_life_index != 0]
    qol_compiled_df.to_csv('Numbeo_API_Data/Qol_compiled.csv')
    
    values = qol_compiled_df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    values_scaled = min_max_scaler.fit_transform(values)
    qol_normal_df = pd.DataFrame(values_scaled, columns=qol_compiled_df.columns, index=qol_compiled_df.index)
    qol_normal_df = city_state_separate(qol_normal_df.reset_index())
    qol_normal_df.set_index('index', inplace=True)
    qol_normal_df.to_csv('Numbeo_API_Data/Qol_normal.csv')
    
#    return qol_normal_df
    