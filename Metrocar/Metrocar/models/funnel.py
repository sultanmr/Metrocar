from sqlalchemy import create_engine, text
import pandas as pd
import pg8000
#import psycopg2
#import psycopg2


DATABASE_URI = "postgresql+pg8000://Test:bQNxVzJL4g6u@ep-noisy-flower-846766-pooler.us-east-2.aws.neon.tech/Metrocar"


# DATABASE_URI = 'postgresql://Test:bQNxVzJL4g6u@ep-noisy-flower-846766-pooler.us-east-2.aws.neon.tech/Metrocar'

engine = create_engine(DATABASE_URI)

def get_funnel_data():
    with engine.connect() as connection:
        query = text("""
            SELECT 
                (SELECT COUNT(*) FROM app_downloads) AS downloads,
                (SELECT COUNT(*) FROM signups) AS signups,
                 (SELECT COUNT(DISTINCT ride_id) FROM ride_requests) AS ride_requests,
                (SELECT COUNT(*) FROM ride_requests WHERE dropoff_ts IS NOT NULL) AS completed_rides
            """)
        result = connection.execute(query).fetchone()
        return dict(result)
    

def get_funnel_data2():
    # Replace with actual SQL query
    funnel_data = {
        'stage': ['Downloads', 'Signups', 'Ride Requests', 'Completed Rides'],
        'values': [1000, 800, 600, 400]  # Example data
    }
    return funnel_data