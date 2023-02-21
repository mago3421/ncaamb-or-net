"""
Project: NCAA Men's Basketball
Module: Rate Limited Requester Prediction
Notes: Requires Python 3.6+
"""

import requests
import time

class rateLimitedRequester:
    def __init__(self, rpm=20):
        self.batchRequests = 0
        self.batchEnd = 0
        # Max allowable requests per minute
        self.rpm = rpm
        
    # Limits requests to rpm
    def rlrequest(self, URL):
        # Make request
        data = requests.get(url=URL)
        # Restart timer if requests is at zero
        if self.batchRequests == 0:
            self.batchEnd = time.time() + 60 # 60 seconds in future
        # Increment requests
        self.batchRequests += 1
        # Check if too many requests per minute have been made
        if self.batchRequests >= self.rpm:
            # Check if there is time remaining
            timeRemaining = self.batchEnd - time.time()
            if timeRemaining > 0:
                # Sleep for the minute before returning data
                time.sleep(timeRemaining)
            self.batchRequests = 0
        return data
