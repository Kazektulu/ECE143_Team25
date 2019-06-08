#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script computes all information required for plotting US Map Slider that shows the variation of the discretionary income over all of the US States
#The analysis considers only certain set of occupations namely:
#'Management', 'Computer & Mathematical', 'Healthcare Practitioners & Technical','Office & Administrative Support', 'Installation, Maintenance, & Repair'
#Slider goes over these different occupations
#
######################################################
import pandas as pd
import os

def plot_US_Map_slider():
    '''
    Function to create the data and layout dictionaries needed by plotly for the US Map slider plot
    
    No arguments taken
    
    Return:
        data_slider (list):
            List of dictionaries that contains the data to be plotted
        layout (dict):
            Contains the settings for the layout of the plot
    '''
    current_dir = os.getcwd()
    filepath = current_dir + '\\processed_data\\discretionary_income_col.csv' #set path of the file containing final discretionary income data
    di_df = pd.read_csv(filepath, index_col=0)
    di_df.reset_index(inplace=True)
    di_df['city'], di_df['state_abr'] = di_df['index'].str.split(pat=', ').str
    
    #list of occupations being considered for the analysis
    occupations = ['Management', 'Computer & Mathematical', 'Healthcare Practitioners & Technical','Office & Administrative Support', 'Installation, Maintenance, & Repair']
    
    #colorscheme for the plots - red
    scl = [[0.0, '#fae2e2'],[0.2, '#ff9999'],[0.4, '#fd6868'], \
           [0.6, '#ff1a1a'],[0.8, '#cc0000'],[1.0, '#4d0000']]
    
    data_slider = [] #list to contain data for each of the plots
    
    for entry in occupations:
        di_temp = pd.concat([di_df['state_abr'], di_df[entry]], axis=1)
        di_cm_groups = di_temp.groupby('state_abr')
        di_cm_average = di_cm_groups.mean() #find the average discretionary income for the state
        di_cm_average.reset_index(inplace = True) 
        
        data_occupation = dict(
            type='choropleth', #set type of visualization
            locations = di_cm_average['state_abr'], #assign data for axes
            z=di_cm_average[entry].rename('occupation').astype(float),
            locationmode='USA-states',
            colorscale = scl
            )
        
        data_slider.append(data_occupation) #append data for each of the occupations to a common list
        
    steps = [] #list to hold the steps for slider
    
    for i in range(len(data_slider)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    label=occupations[i]) # label to be displayed for each step (occupation name)
        step['args'][1][i] = True
        steps.append(step)
    
    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]  #create slider object using individual steps
    
    #set up the layout for the visualization including the slider
    layout = dict(geo=dict(scope='usa',
                           projection={'type': 'albers usa'}),
                  sliders=sliders)
        
    return data_slider, layout