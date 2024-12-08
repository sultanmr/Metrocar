import Metrocar.database as db  # Assuming `db.load_data` is in Metrocar.database
import Metrocar.visualizations.funnel as funnel_viz

def test_load_data():
    tables_to_test = db.get_table_names()
    #["transactions", "signups", "ride_requests", "app_downloads"]
    for table_name in tables_to_test:
        try:
            # Load data for the table
            data = db.load_data(table_name)
            print(f"Data for {table_name}:")
            print(data.head())  # Print the first few rows if it's a DataFrame
            print("\n")
        except Exception as e:
            print(f"Error loading data for table '{table_name}': {e}")

def test_funnel():
    app_downloads = db.load_data("app_downloads")
    signups = db.load_data("signups")
    ride_requests = db.load_data("ride_requests")
    transactions = db.load_data("transactions")
    funnel_viz.create_funnel(app_downloads, signups, ride_requests, transactions)
    print (funnel_viz)

def save_data_locally():
    tables_to_test = db.get_table_names()
    #["transactions", "signups", "ride_requests", "app_downloads"]
    for table_name in tables_to_test:
        try:
            # Load data for the table
            data = db.load_data(table_name)
            print(f"Data for {table_name}:")
            data.to_csv(f'{table_name}.csv', index=False)
            
        except Exception as e:
            print(f"Error loading data for table '{table_name}': {e}")

    
if __name__ == "__main__":
    save_data_locally()
