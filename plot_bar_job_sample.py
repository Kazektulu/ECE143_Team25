#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script includes the functions needed to plot bar plots for comparing the salary components of the job prospects
#Data and layout generated can be used to plot the visual using plotly
#
######################################################

import os
import pandas as pd
import plotly.graph_objs as go

def bar_plot_data_format1():
    '''
    Function to format the data for the income breakdown bar plot
    
    Returns:
        List containing Salary, Cost of living, Federal Tax and State Tax for each of the four jobs in the use case
        This can be further forwarded to the bar graph plotter for constructing the visualizations
    '''
    
    current_dir = os.getcwd()
    filepath = current_dir + '\\processed_data\\job_samples_di_components.csv' #set path of the file containing job sample component data which was manually collected from the final discretionary income dataset
    job_sample_df = pd.read_csv(filepath, index_col=3)
    

    new_york = job_sample_df.loc[['New York']].values.tolist()[0][4:8]
    san_francisco = job_sample_df.loc[['San Francisco']].values.tolist()[0][4:8]
    austin = job_sample_df.loc[['Austin']].values.tolist()[0][4:8]
    raleigh = job_sample_df.loc[['Raleigh']].values.tolist()[0][4:8]
    
    Income = ["Salary","Cost of Living","Federal Tax", "State Tax"]
    
    return new_york, san_francisco, austin, raleigh, Income

def bar_plot_data_format2():
    '''
    Function to format the data for the discretionary income and quality of life bar plot
    
    Returns:
        List containing Discretionary Income and Quality of Life (Scaled for better visualization) for each of the four jobs in the use case
        This can be further forwarded to the bar graph plotter for constructing the visualizations
    '''
    
    current_dir = os.getcwd()
    filepath = current_dir + '\\processed_data\\job_samples_di_components.csv' #set path of the file containing job sample component data which was manually collected from the final discretionary income dataset
    job_sample_df = pd.read_csv(filepath, index_col=3)
    
    job_sample_df['qol'] = job_sample_df['qol'] * 100
    new_york = job_sample_df.loc[['New York']].values.tolist()[0][8:]
    san_francisco = job_sample_df.loc[['San Francisco']].values.tolist()[0][8:]
    austin = job_sample_df.loc[['Austin']].values.tolist()[0][8:]
    raleigh = job_sample_df.loc[['Raleigh']].values.tolist()[0][8:]
    
    Income = ["Discretionary Income", "Quality of Life Index"]
    
    return new_york, san_francisco, austin, raleigh, Income

def bar_plot_trace_create(Income, NY, SF, TX, NC, title):
    '''
    Function to create the traces for the bar plots which can then be visualized using plotly
    
    Arguments:
        Income (list):
            x axis labels
        NY (list):
            component values for NY
        SF (list):
            component values for SF
        TX (list):
            component values for TX
        NC (list):
            component values for NC
        title (str):
            title of the graph
    
    Returns:
        data (list):
            List of dictionaries that contains data for all four traces
        layout (dict):
            Layout information for the bar plot
    '''
    
    trace1 = go.Bar(
        x=Income,
        y=NY,
        name='New York',
        width=[0.2,0.2,0.2,0.2]
    )
    trace2 = go.Bar(
        x=Income,
        y=SF,
        name='San Francisco',
        width=[0.2,0.2,0.2,0.2]
    )
    trace3 = go.Bar(
        x=Income,
        y=TX,
        name='Austin',
        width=[0.2,0.2,0.2,0.2]
    )
    trace4 = go.Bar(
        x=Income,
        y=NC,
        name='Raleigh',
        width=[0.2,0.2,0.2,0.2]
    )
    
    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        title = title,
        yaxis = dict(title = 'Amount (USD)'),
        barmode='group',
        bargap=0.3,
        font = {'size':14}
    )
    
    return data, layout

    
    
    