from plotly.offline import init_notebook_mode, plot
init_notebook_mode(connected='True')
import pandas as pd
import numpy as np
import plotly.io as pio

excel_path = 'C:/ECE143Project/state_avg.csv'#You should change it with your own path
x_discretionary_average = pd.read_csv(excel_path)#This is the salary data

df=x_discretionary_average
'''
The following code is used to implement the discretionary income
'''

#state_name=x_discretionary_average['state_name']
#x_discretionary_average = x_discretionary_average.drop('state_name', axis=1)
#x_discretionary_average .insert(0, 'state_name', state_name)
#x_discretionary_average.to_csv('C:/ECE143Project/Discretionary_Income_average.csv')

#state_name=x_discretionary_average['state_name']

#for i in range(len(state_name)):
 #   state_name[i]=state_name[i].replace(' ','')#This code is used to delete ' '
  #  state_name[i]=state_name[i].split(',',1)[1]#state_new only has the state information
    
#x_discretionary_average.to_csv('C:/ECE143Project/Discretionary_Income_average.csv')

#g = x_discretionary_average.groupby(x_discretionary_average['state_name'])#group by state
#state_avg=g.mean()

#state_avg.to_csv('C:/ECE143Project/state_avg.csv')
'''
The following is used to generate US map plot
'''

for col in df.columns:
    df[col] = df[col].astype(str)

# set color
colorscale = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

# 
#df['text'] = df['state'] + '<br>' +\
  #  'Beef '+df['beef']+' Dairy '+df['dairy']+'<br>'+\
  #  'Fruits '+df['total fruits']+' Veggies ' + df['total veggies']+'<br>'+\
  #  'Wheat '+df['wheat']+' Corn '+df['corn']

data = [ dict(
        type='choropleth',
        colorscale = colorscale,
        autocolorscale = False,
        # 
        locations = df['state_name'],
        # 
        z = df['Discretionary_Income_average'].astype(float),
        locationmode = 'USA-states',
        #text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        # 
        colorbar = dict(
            title = "USD")
        ) ]

layout = dict(
        title = 'The average discretionary Income',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' )
        )
)
    
fig = dict( data=data, layout=layout )
plot(fig,image='jpeg')

pio.write_image(fig, 'C:/ECE143Project/fig1.jpeg',width=1400, height=800, scale=8)


        
        