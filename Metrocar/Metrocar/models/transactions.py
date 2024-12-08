# models/transactions.py

class Transactions:
    def __init__(self, df):
        self.df = df

    def get_completed_rides (self):
        return (self.df['charge_status'] == 'Approved').sum()

    def get_price_bins (self):
        return ['All', '10-14', '15-19', '20-24', '25-30']