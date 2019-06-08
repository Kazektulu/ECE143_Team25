#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script includes the functions needed to plot line charts for analysis of trends in income components for different regions of US
#
######################################################
import plotly.graph_objs as go
from plotly import tools

def plot_line_chart_trace(states1, col1, qol1, states2, col2, qol2, states3, col3, qol3, trace_odd, trace_even):
    '''
    This function sets up the fig dictionary that can be used by plotly to visualize the line plots
    '''
    
    trace1 = go.Scatter(
        x=states1,
        y=col1,
        legendgroup='a',
        name=trace_odd,
        marker={'color':'steelblue'}
    )
    
    trace2 = go.Scatter(
        x=states1,
        y=qol1,
        legendgroup='b',
        name=trace_even,
        marker={'color':'orange'}
    )
    
    trace3 = go.Scatter(
        x=states2,
        y=col2,
        legendgroup='a',
        showlegend=False,
        name=trace_odd,
        marker={'color':'steelblue'}
    )
    
    trace4 = go.Scatter(
        x=states2,
        y=qol2,
        legendgroup='b',
        showlegend=False,
        name=trace_even,
        marker={'color':'orange'}
    )
    
    trace5 = go.Scatter(
        x=states3,
        y=col3,
        legendgroup='a',
        showlegend=False,
        name=trace_odd,
        marker={'color':'steelblue'}
    )
    
    trace6 = go.Scatter(
        x=states3,
        y=qol3,
        legendgroup='b',
        showlegend=False,
        name=trace_even,
        marker={'color':'orange'}
    )
    
    fig = tools.make_subplots(rows=2, cols=2, specs=[[{}, {}], [{'colspan': 2}, None]],
                          subplot_titles=('Trends in Central US','Trends in West US', 'Trends in East US'))

    fig.append_trace(trace5, 1, 1)
    fig.append_trace(trace6, 1, 1)
    fig.append_trace(trace3, 1, 2)
    fig.append_trace(trace4, 1, 2)
    fig.append_trace(trace1, 2, 1)
    fig.append_trace(trace2, 2, 1)
    
    return fig