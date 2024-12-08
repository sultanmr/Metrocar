import plotly.graph_objs as go
from plotly.io import to_json

def create_ride_distribution(ride_requests):
    ride_distribution = ride_requests.get_ride_requests_by_hour()

    ride_fig = go.Figure(
        go.Bar(
            x=ride_distribution.index,
            y=ride_distribution.values,
            marker=dict(color='skyblue')
        )
    )
    ride_fig.update_layout(title="Ride Requests by Hour", xaxis_title="Hour of Day", yaxis_title="Requests")
    return to_json(ride_fig)
