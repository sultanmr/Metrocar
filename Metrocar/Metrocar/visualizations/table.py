import plotly.graph_objects as go
import pandas as pd

def create_table_view(data, title="Table View"):
    """
    Create a table visualization using Plotly.
    
    Parameters:
        data (pd.DataFrame): The data to display in the table.
        title (str): The title of the table.

    Returns:
        str: A JSON object for Plotly to render in the frontend.
    """
    if data.empty:
        return go.Figure().to_json()

    # Create a table with Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(data.columns),
            fill_color='lightblue',
            align='left',
            font=dict(size=12, color='black')
        ),
        cells=dict(
            values=[data[col] for col in data.columns],
            fill_color='lightgrey',
            align='left',
            font=dict(size=11, color='black')
        )
    )])

    # Add a title
    fig.update_layout(title_text=title, title_x=0.5)
    return fig.to_json()
