import pandas as pd

class Reviews:
    def __init__(self, data):
        self.data = data

    def get_rating(self):            
        # ratings = self.data['rating'].unique().tolist()
        # ratings.insert(0, "All") 
        # return ratings
        return ['All', '1', '2', '3', '4', '5']