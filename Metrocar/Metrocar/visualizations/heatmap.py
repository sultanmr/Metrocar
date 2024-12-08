import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import numpy as np

def render_heatmap (data):    
    
    formatted_index = [str(item).replace('_', ' ').title() for item in data.index.tolist()]
    formatted_columns = [str(item).replace('_', ' ').title() for item in data.columns.tolist()]

    heatmap = go.Heatmap(
        z=data.values, 
        colorscale='greens'
    )

    layout = go.Layout(    
        yaxis=dict(        
            tickvals=np.arange(len(data.index)),  
            ticktext=formatted_index 
        ),
        xaxis=dict(        
            tickvals=np.arange(len(data.columns)),  
            ticktext=formatted_columns  
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return go.Figure(data=[heatmap], layout=layout)

def get_fig(data, group_name):    
    return render_heatmap(data)

