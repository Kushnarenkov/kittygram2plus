from rest_framework import throttling

import datetime as dt

class WorkingHoursRateThrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        now = dt.datetime.now().hour
        if now >= 3 and now <= 5:
            return False
        return True