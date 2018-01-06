import datetime, random
from entry import Entry
from cal import Calendar
class Page:
    def __init__(questions = 100, date = datetime.datetime.now()):
        # make questions
        self.questions = 100
        self.entries = []

        if date.day == -1
        date
        self.date = date

        self.cal = Calendar(questions, self.date.)

        for i in range(self.questions):
            entries.append(Entry(get_date(i), get_time(i)))




    def get_date(self, index):

    def get_time(self, index):

    def make_content(self):



    def get_num_qs(self):
        pct_single = 95
        pct_double = 4
        pct_triple = 1

        randy = random.random()*(pct_single + pct_double +  pct_triple)

        if randy < pct_single:
            num_qs = 1;
        elif randy < pct_single + pct_double:
            num_qs = 2
        else:
            num_qs = 3

        return num_qs
