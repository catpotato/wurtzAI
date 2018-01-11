import random, datetime
from calendar import monthrange
from math import floor
class Calendar:
    '''

    decides the time and day that each question will occur at, for now this is random

    '''
    def __init__(self, dt):
        self.submitted_dist = [0] * days
        self.dt = dt
        self.days = monthrange(dt.year, dt.month)
        self.genarated_dist = [0] * days

    def add_entry(self, dt):
        self.submitted_dist[dt.day] += 1


    def genarate(self, qs):
        # stars by populating every day with one question
        dist = [1] * days
        double_pct =.3

        # adds a question to each day if the pct says it should
        while qs != 0:
            for i in range(self.days):
                if random.random() < (double_pct/self.submitted_dist[i]+1) :
                    dist[i] += 1
                    qs -=1

        # once all the questions are depleted we are done
        self.genarated_dist = dist


    def get_next_entry(self):
        day = 0
        for i, allowed_qs in enumerate(self.genarated_dist):
            if allowed_qs != 0:
                self.genarated_dist[i] -=1
                day = i + 1
                break

        dt = self.dt
        dt.day = day

        # randomize date and time
        dt.hour = floor(random.random()*24)
        dt.minute = floor(random.random()*60)
        dt.second = floor(random.random()*60)

        return dt
