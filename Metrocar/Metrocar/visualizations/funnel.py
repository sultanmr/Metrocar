import plotly.graph_objs as go
from plotly.io import to_json
import pandas as pd
import colorsys


base_color = '#006400'
report_columns = ['signedup_users', 'ride_request', 'ride_accepted', 'ride_finished', 'ride_paid', 'ride_reviewed']
report_columns_names = [name.replace('_', ' ').title() for name in report_columns]

def generate_color_gradients(base_color, num_colors):
    # Convert hex to RGB
    r, g, b = int(base_color[1:3], 16), int(base_color[3:5], 16), int(base_color[5:7], 16)
    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    colors = []
    if num_colors<=1:
      num_colors = 2
    for i in range(num_colors):
        # Increase value (brightness) for each color
        new_v = min(1, v + (1 - v) * (i / (num_colors - 1)))
        # Convert back to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, new_v)
        # Convert to hex
        colors.append('#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255)))
    return colors

def render_funnel(funnel_group):
    global report_columns_names    
    global base_color
    
    platform_colors = generate_color_gradients(base_color, len(funnel_group.index))
    fig = go.Figure()

    for platform, color in zip(funnel_group.index, platform_colors):
        fig.add_trace(go.Funnel(
            name=platform,
            y=report_columns_names,
            x=funnel_group.loc[platform],
            textinfo="value+percent initial",
            marker=dict(color=color)
        ))    
    fig.update_layout(
        #title="Funnel Chart by Platform",
        #showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)' 
    )
    return fig


def get_fig(data, group_name):
    return render_funnel(data)

    