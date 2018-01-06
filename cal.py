import random
class Calendar:
    '''

    decides the time and day that each question will occur at, for now this is random

    '''
    def __init__(self, days, questions):

        # stars by populating every day with one question
        dist = [1] * days
        double_pct =.3

        qs = questions

        # adds a question to each day if the pct says it should
        while qs != 0:
            for i in range(days):
                if random.random() < double_pct:
                    dist[i] += 1
                    qs -=1
        # once all the questions are depleted we are done
        self.dist = dist

    def get_day(self, day):
        return self.dist[day+1]
