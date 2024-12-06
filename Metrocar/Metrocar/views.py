from datetime import datetime
from flask import render_template
from Metrocar import app

from flask import Flask, render_template, jsonify

import plotly.express as px
import plotly.io as pio
from Metrocar.models.funnel import get_funnel_data
from Metrocar.models.funnel import get_funnel_data2
import plotly.graph_objs as go
from plotly.io import to_json

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/funnel')
def funnel():
    """Render the funnel chart page."""
    funnel_data = get_funnel_data()

    stages = ["App Downloads", "Signups", "Ride Requests", "Completed Rides"]
    values = [
        funnel_data['downloads'],
        funnel_data['signups'],
        funnel_data['ride_requests'],
        funnel_data['completed_rides']
    ]

    fig = px.funnel(
        x=values,
        y=stages,
        title="User Journey Funnel",
        labels={"x": "Count", "y": "Stages"}
    )

    graph_html = pio.to_html(fig, full_html=False)

    return render_template('funnel.html', graph_html=graph_html, title="Funnel Chart")



@app.route('/dashboard')
def dashboard():
    # Example: Funnel visualization data
    funnel_data = get_funnel_data2()
    funnel_fig = go.Figure(
        go.Funnel(
            y=funnel_data['stage'],
            x=funnel_data['values']
        )
    )
    funnel_json = to_json(funnel_fig)

    return render_template('dashboard.html', funnel_json=funnel_json)