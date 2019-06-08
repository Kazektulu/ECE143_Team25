#
# ECE 143 Project - Discretionary Income Analysis Tool
#
######################################################
#
#This script includes the functions needed to plot pie chart for comparing the salary components of the top two job prospects
#Fig dictionary generated can be used to plot the visual using plotly
#
######################################################

def plot_pie_chart():
    '''
    This function is used to create fig dictionary that can then be used for visualization using plotly
    
    Returns:
        fig(dict)
    '''
    fig = {
      "data": [
        {
          "values": [30502.8, 0, 35108.09, 61484.11],
          "labels": [
            "Federal Tax",
            "State Tax",
            "Cost of Living",
            "Discretionary Income"
          ],
          "domain": {"column": 0},
          "hoverinfo":"label+percent+value",
          "hole": .4,
          "type": "pie"
        },
        {
          "values": [26890.8, 5882.3625, 28685.95119, 50585.88631],
          "labels": [
            "Federal Tax",
            "State Tax",
            "Cost of Living",
            "Discretionary Income"
          ],
          "domain": {"column": 1},
          "hoverinfo":"label+percent+value",
          "hole": .4,
          "type": "pie"
        }],
      "layout": {
            "title":"Income Breakdown for Top Two Contenders",
            "grid": {"rows": 1, "columns": 2},
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Austin<br>TX",
                    "x": 0.185,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Raleigh<br>NC",
                    "x": 0.82,
                    "y": 0.5
                }
            ]
        }
    }
        
    return fig