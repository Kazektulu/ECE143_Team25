#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script includes the functions needed to plot bar charts for comparing discretionary income of metropolitan cities with its neighboring cities having better quality of life
#One function sets up the data while the other sets up traces and layout taht can be used by plotly to visualize
#
######################################################
import pandas as pd
import plotly.graph_objs as go
import os

def plot_metropolitan_data():
    '''
    Function computes the data that is to be plotted for the comparison of metropolitan cities with the neighboring cities in same state
    Returns:
        Discretionary income data for each of the cities in teh four states along with the x axis labels
    '''
    
    current_dir = os.getcwd()
    filepath = current_dir + '\\raw_data\\col_di_metropolitan_manual.xlsx' #set path of the file containing job sample component data which was manually collected from the final discretionary income dataset

    main_cities = pd.read_excel(filepath)
    main_cities_groups = main_cities.groupby('State', sort=False)
    dict_city_di = [[],[],[]]

    for group in main_cities_groups:
        for i in range(3):
            dict_city_di[i].append(group[1]['DI'].values.tolist()[i])
            
    Cities = ["New York", "California", "Texas", "Florida"]
    city1 = dict_city_di[0]
    city2 = dict_city_di[1]
    city3 = dict_city_di[2]
    
    return Cities, city1, city2, city3

def plot_metropolitan_trace(Cities, city1, city2, city3, color1, color2, color3):
    '''
    Function computes the data and layout dictionaries that can be used by plotly for visualization
    
    Arguments:
        Color scheme for the four states under consideration
        
    Returns:
        data (list):
            list of dictionaries for the traces for all four states
        layout (dict):
            dictionary for the layout setup for plotly visualization
    '''
    
    trace1 = go.Bar(
        x=Cities,
        y=city1,
        name='High<br>Population City',
        text=['New York City', 'Los Angeles', 'Houston', 'Jacksonville'],
        hoverinfo= 'text',
        marker=dict(color=color1),
    )
    trace2 = go.Bar(
        x=Cities,
        y=city2,
        name='Medium<br>Population City',
        text=['Albany','San Diego','Austin','Melbourne'],
        hoverinfo= 'text',
        marker=dict(color=color2)
    )
    trace3 = go.Bar(
        x=Cities,
        y=city3,
        name='Low<br>Population City',
        text=['Syracuse','Santa Barbara','El Paso','Sarasota'],
        hoverinfo = 'text',
        marker=dict(color=color3)
    )
    
    data = [trace1, trace2, trace3]
    layout = go.Layout(
        title = 'Discretionary Income Trends in Prominent States',
        barmode='group',
        bargap=0.4,
        font = {'size':14},
        yaxis = dict(title = 'Discretionary Income (USD)', titlefont={'size':15})
    )
    
    return data, layout

    
    
