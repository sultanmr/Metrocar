from flask import Blueprint, render_template, jsonify, request, current_app
import plotly.io as pio
import threading
import time

import Metrocar.models as models
import Metrocar.visualizations.funnel as funnel_viz
import Metrocar.visualizations.ride_distribution as ride_viz
import Metrocar.visualizations.age_group as age_group_viz
import Metrocar.visualizations.platform as platform_viz
import Metrocar.visualizations.table as table_viz
import Metrocar.database as db

# Define the blueprint
views_blueprint = Blueprint('views', __name__)

# Globals
app_downloads, signups, ride_requests, transactions, reviews = None, None, None, None, None
all_data = None
loaded = False
platforms = []
age_ranges = []
# @views_blueprint.before_request
# def initialize_data_before_request():    
#     load_data()
    
def load_data ():
    global all_data, app_downloads, signups, ride_requests, transactions, reviews, loaded
    global platforms, age_ranges
    if loaded:
        return
    with current_app.app_context():
        if app_downloads is None:
            df = db.load_data("app_downloads")
            app_downloads = models.AppDownloads(df)
            platforms = app_downloads.get_platforms()
        if signups is None:
            df = db.load_data("signups")
            signups = models.Signups(df)
            age_ranges = signups.get_age_ranges()
        if ride_requests is None:
            df = db.load_data("ride_requests")
            ride_requests = models.RideRequests (df)
        if transactions is None:
            df = db.load_data("transactions")
            transactions = models.Transactions(df)
        if reviews is None:
            reviews = db.load_data("reviews")
        all_data = db.merge_data()
        loaded = True

@views_blueprint.route('/')
def index_page():
    return render_template('loading.html')
   

@views_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard_view():
    global all_data
    # global platforms, age_ranges
    # Load the data
    load_data()
    
    print (request.method)
    # Handle filtering on POST
    if request.method != 'POST':
        return default_dashboard()

    data = request.get_json()
    platforms = data.get('platforms', [])
    age_ranges = data.get('age_ranges', [])
    
    if not platforms and not age_ranges:
        return default_dashboard()

    all_defaults = 'All' in platforms and 'All' in age_ranges
    if all_defaults:
        return jsonify(get_funnel_data(all_data))         
    
    filtered_df = all_data.copy()

    if platforms and not 'All' in platforms:
        print (f"filtering...{platforms}")
        filtered_df = filtered_df[filtered_df['platform'].isin(platforms)]
    if age_ranges and not 'All' in age_ranges:
        print (f"filtering...{age_ranges}")
        filtered_df = filtered_df[filtered_df['age_range'].isin(age_ranges)]
        
    try:            
        return jsonify(get_funnel_data(filtered_df))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
   
def get_funnel_data (data):   
    global platforms, age_ranges

    if data.empty:
        print("Filtered DataFrame is empty.")
        
    funnel_fig = funnel_viz.create_platform_funnel(data)  
    graph_html = pio.to_html(funnel_fig, full_html=False, include_plotlyjs="cdn")
    return {'graph_html': graph_html}

def default_dashboard ():
    global all_data
    global platforms, age_ranges
    try:
        funnel_fig = funnel_viz.create_platform_funnel(all_data)   
        
        return render_template(
            'funnel.html',
            title="Platform Funnel",            
            platforms=platforms,
            age_ranges = age_ranges,
            graph_html = pio.to_html(funnel_fig, full_html=False),
            df_data = "default_dashboard"
        )
    except Exception as e:
        return f"An error occurred: {e}", 500

