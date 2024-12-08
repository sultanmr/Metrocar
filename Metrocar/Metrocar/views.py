from flask import Blueprint, render_template, jsonify, request, current_app
import plotly.io as pio
import pandas as pd
# import threading
# import time

import Metrocar.models as models
import Metrocar.visualizations.funnel as funnel_viz
import Metrocar.visualizations.heatmap as heatmap_viz


import Metrocar.database as db

views_blueprint = Blueprint('views', __name__)

# Globals
app_downloads, signups, ride_requests, transactions, reviews = None, None, None, None, None
all_data = None
loaded = False
report_columns = ['signedup_users', 'ride_request', 'ride_finished', 'ride_paid', 'ride_reviewed']
filters_list = ['platform', 'age_range', 'rating', 'purchase_amount_usd']
filter_data_dict = {}
default_funnel_type = 'platform'
funnel_type = default_funnel_type

# @views_blueprint.before_request
# def initialize_data_before_request():    
#     load_data()

    
def load_data ():
    global all_data, app_downloads, signups, ride_requests, transactions, reviews, loaded
    global filter_data_dict
    if loaded:
        return
    with current_app.app_context():
        if app_downloads is None:
            df = db.load_data("app_downloads")
            app_downloads = models.AppDownloads(df)          
            filter_data_dict['platform'] = app_downloads.get_platforms()
        if signups is None:
            df = db.load_data("signups")
            signups = models.Signups(df)
            filter_data_dict['age_range'] = signups.get_age_ranges()
        if ride_requests is None:
            df = db.load_data("ride_requests")
            ride_requests = models.RideRequests (df)
        if transactions is None:
            df = db.load_data("transactions")
            transactions = models.Transactions(df)
            filter_data_dict['purchase_amount_usd'] = transactions.get_price_bins()
        if reviews is None:
            df = db.load_data("reviews")
            reviews = models.Reviews (df)
            filter_data_dict['rating'] = reviews.get_rating()
        all_data = db.merge_data()
        loaded = True

@views_blueprint.route('/')
def index_page():
    return render_template('loading.html')
   

@views_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard_view():
    global all_data, filters_list, filter_data_dict, funnel_type
    global report_columns   

    load_data()

    if request.method != 'POST':
        return default_dashboard()

    data = request.get_json()
    
    filtered_df = all_data.copy()
    all_price_df = None
    funnel_type = data.get('funnel_type', default_funnel_type)
       
    
    all_defaults = all(
        filter_values == ['All'] for filter_values in (data.get(filter_name, ['All']) for filter_name in filters_list)
    )    
    
    # local_filters = {filter_name: data.get(filter_name, ['All']) or ['All'] for filter_name in filters_list}
    
    # for filter_name, filter_values in local_filters.items():        
    #     print(f"Filtering {filter_name} with values: {filter_values}")            


    
    
    if all_defaults:   
        return default_dashboard()

    for filter_name in filters_list:
        filter_values = data.get(filter_name, ['All'])
        
        if filter_name=='rating' and 'All' not in filter_values:
            filter_values = [int(value) for value in filter_values]
          
        if filter_values and 'All' not in filter_values:
            print(f"Filtering {filter_name} with values: {filter_values}")
            if filter_name=='purchase_amount_usd':

                for filter_value in filter_values:
                    lower_bound, upper_bound = map(float, filter_value.split('-'))
                    price_df = filtered_df[
                        (filtered_df['purchase_amount_usd'] >= lower_bound) &
                        (filtered_df['purchase_amount_usd'] <= upper_bound)
                    ]
                    if all_price_df is None:
                        all_price_df = price_df.copy() 
                    else:
                        all_price_df = pd.concat([all_price_df, price_df])                
            else:               
                filtered_df = filtered_df[filtered_df[filter_name].isin(filter_values)]

    if all_price_df is not None:        
        filtered_df =  pd.merge(filtered_df, all_price_df, how='inner').drop_duplicates()        

    
    if filtered_df.empty:       
        return default_dashboard()
        

    grouped_data = filtered_df.groupby(funnel_type)[report_columns].sum()


    
    try: 
        return jsonify({
            'funnel_html': get_html_data(funnel_viz, grouped_data), 
            'heatmap_html': get_html_data(heatmap_viz, grouped_data)
          
         })
      
    except Exception as e:
        print (e)
        return jsonify({'error': str(e)}), 500
    
def default_dashboard ():
    global all_data, report_columns    
    global funnel_type

    grouped_data = all_data.groupby(funnel_type)[report_columns].sum()

    try:
        return render_template(
            'dashboard.html',
            title="Funnel",            
            platform=filter_data_dict['platform'],
            age_range = filter_data_dict['age_range'],
            rating = filter_data_dict['rating'],
            purchase_amount_usd = filter_data_dict['purchase_amount_usd'],
            funnel_html = get_html_data(funnel_viz, grouped_data),   
            heatmap_html = get_html_data(heatmap_viz, grouped_data)  
        )
      
      
    except Exception as e:
        print (e)
        return f"An error occurred: {e}", 500


def get_html_data (viz, data): 
    global funnel_type
    fig = viz.get_fig(data, funnel_type)  
    return pio.to_html(fig, full_html=False, include_plotlyjs="cdn")
    #return pio.to_html(fig, full_html=False)
    

