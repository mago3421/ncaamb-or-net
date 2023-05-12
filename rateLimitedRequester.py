"""
Project: NCAA Men's Basketball
Module: Rate Limited Requester Prediction
Notes: Requires Python 3.6+
"""

import urllib
import time

class rateLimitedRequester:
    def __init__(self, rpm=20):
        self.batchRequests = 0
        self.batchEnd = 0
        # Max allowable requests per minute
        self.rpm = rpm

    def rlrequest(self, URL):
        try:
            data = urllib.request.urlopen(URL).read()
        except Exception:
            return None
        time.sleep(3)
        return data

"""     
    # Limits requests to rpm
    def rlrequest(self, URL):
        # Check if too many requests per minute have been made
        if self.batchRequests >= self.rpm:
            # Check if there is time remaining
            timeRemaining = self.batchEnd - time.time()
            if timeRemaining > 0.0:
                # Sleep for the minute before making request
                time.sleep(timeRemaining)
            self.batchRequests = 0
        # Make request
        data = urllib.request.urlopen(URL).read()
        # Restart timer if requests is at zero
        if self.batchRequests == 0:
            self.batchEnd = time.time() + 60.0
        # Increment requests
        self.batchRequests += 1         
        return data
"""

