import pandas as pd

class RideRequests:
    def __init__(self, data):
        self.data = data

    def get_ride_request_count(self):
        return self.data['ride_id'].nunique()

    def get_ride_requests_by_hour(self):
        self.data['hour'] = self.data['request_ts'].dt.hour
        return self.data.groupby('hour').size()
