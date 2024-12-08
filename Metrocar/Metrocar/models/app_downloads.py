import pandas as pd

class AppDownloads:
    def __init__(self, data):
        self.data = data
    
    def get_platform_distribution(self):
        platform_distribution = self.data['platform'].value_counts()
        return platform_distribution

    def get_platforms(self):            
        platforms = self.data['platform'].unique().tolist()
        platforms.insert(0, "All") 
        return platforms
