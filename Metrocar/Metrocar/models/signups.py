# models/signups.py

class Signups:
    def __init__(self, data):
        """
        Initializes the Signups model with data.
        :param data: Data source (could be a list of dicts, dataframe, etc.)
        """
        self.data = data

    def get_signup_count(self):
        """
        Returns the number of signups in the data.
        """
        return len(self.data)

    def get_age_ranges(self):
        return ['All', '18-24', '25-34', '35-44', '45-54', 'Unknown']
        # age_ranges = self.data['age_range'].unique().tolist()
        # age_ranges.insert(0, "All") 
        # return age_ranges
    
    def get_signup_by_platform(self):
        """
        Returns a breakdown of signups by platform (iOS, Android, Web).
        Assumes 'platform' is a field in the data.
        """
        platform_count = {}
        for signup in self.data:
            platform = signup.get('platform')
            if platform:
                platform_count[platform] = platform_count.get(platform, 0) + 1
        return platform_count

    def get_age_group_signup_count(self):
        """
        Returns the count of signups by age group.
        Assumes 'age_range' is a field in the data.
        """
        age_group_count = {}
        for signup in self.data:
            age_range = signup.get('age_range')
            if age_range:
                age_group_count[age_range] = age_group_count.get(age_range, 0) + 1
        return age_group_count

    def get_signup_dates(self):
        """
        Returns the list of signup timestamps.
        Assumes 'signup_ts' is a field in the data.
        """
        return [signup.get('signup_ts') for signup in self.data]
