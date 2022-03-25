# Heather Antwine 000425323

import collections
import random
from settings import *


# Clock class for the simulation time
class Clock:
    def __init__(self, hr, min, sec):
        self.hr = hr
        self.min = min
        self.sec = sec

    # O(1) runtime for returning the clock in string type
    def __str__(self):
        return " %d:%02d:%02d %s" % (self.hr_mod(), self.min, self.sec, ("AM", "PM")[self.hr >= 12])

    # O(1) runtime for proper time format - secs > mins > hrs
    def sec_tick(self):
        self.sec = self.sec + 1
        if self.sec >= 60:
            self.sec = 0
            self.min = self.min + 1
            if self.min >= 60:
                self.min = 0
                self.hr = self.hr + 1
                if self.hr >= 24:
                    self.hr = 0

    # O(1) runtime for comparing current time and the input_time
    def compare_time(self, input_time):
        input_time = [int(x) for x in list(input_time.split(':'))]
        return self.hr == input_time[0] and \
            self.min == input_time[1] and \
            self.sec == input_time[2]

    # O(1) runtime for returning time in standard format - non-military format
    def hr_mod(self):
        return ((self.hr-1) % 12)+1

    # O(1) runtime for setting the time on the clock to the input_time
    def set_time(self, input_time):
        input_time = [int(x) for x in list(input_time.split(':'))]
        self.hr = input_time[0]
        self.min = input_time[1]
        self.sec = input_time[2]

        # TODO