# models/transactions.py

class Transactions:
    def __init__(self, df):
        """
        Initializes the Transactions model with df.
        :param df: df source (could be a list of dicts, dfframe, etc.)
        """
        self.df = df

    def get_transaction_count(self):
        """
        Returns the number of transactions in the df.
        """
        return len(self.df)

    def get_total_revenue(self):
        """
        Returns the total revenue from all transactions.
        Assumes 'purchased_amount_usd' is a field in the df.
        """
        total_revenue = sum(transaction.get('purchased_amount_usd', 0) for transaction in self.df)
        return total_revenue

    def get_transaction_status_count(self):
        """
        Returns a breakdown of transaction statuses (e.g., completed, failed).
        Assumes 'charge_status' is a field in the df.
        """
        status_count = {}
        for transaction in self.df:
            status = transaction.get('charge_status')
            if status:
                status_count[status] = status_count.get(status, 0) + 1
        return status_count

    def get_transactions_by_date(self):
        """
        Returns a list of transaction timestamps.
        Assumes 'transaction_ts' is a field in the df.
        """
        return [transaction.get('transaction_ts') for transaction in self.df]

    def get_high_value_transactions(self, threshold=50):
        """
        Returns transactions where the purchased amount is greater than the threshold.
        :param threshold: The amount above which a transaction is considered 'high value'.
        """
        return [transaction for transaction in self.df if transaction.get('purchased_amount_usd', 0) > threshold]

    def get_completed_rides (self):
        return (self.df['charge_status'] == 'Approved').sum()