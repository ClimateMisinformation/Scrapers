import time


class timetraker(start_time, end_time, function_name, functionality):
    """ Tracks time and reports consistently:"""

    def __init__(self, start_time, end_time, function_name, functionality):
        self.start_time = start_time
        self.end_time = end_time
        self.function_name = function_name
        self.time_taken = 0

    def calculate(self, start_time, end_time, functionality):
        """ 
        start_time: Time when the function started
        end_time: Time when the function finished
        """
        self.time_taken = end_time - start_time
