import datetime, random
from entry import Entry
from cal import Calendar

from sqlalchemy import create_engine, select, Table, Column, Integer, Numeric, String, func
from dbmodel import table_genarated, table_submitted

class Page:
    def __init__(questions = 100, dt = datetime.datetime.now()):
        # make questions
        self.questions = 100
        self.entries = []
        self.dt = dt
        self.cal = Calendar(dt)

        self.fill()

    def fill(self):
        # first, determine how many questions are in the real database for this time period

        # open up database

        engine = create_engine('sqlite:///data.db', echo=True)
        metadata = MetaData()

        submitted = table_submitted(metadata)

        # get all data from this month
        s = select([submitted]).where(cookies.c.month == self.date.month)
        submitted_entries = connection.execute(s)

        # if the amount is less than we want
        num_genarated = self.questions - rp.count()
        genarated_entries = self.genarate(num_genarated, metadata)

        # add the submitted q's in first, tell calendar where things lie

        # add these bad boys into entries
        for entry in submitted_entries:
            self.add_submitted_entry(entry)

        # tell calendar it can now fill things up
        self.cal.genarate(num_genarated)

        # fill up the entries with fake components
        for entry in genarated_entries:
            self.add_genarated_entry

        # order all entries by date
        entries = sorted(entries, key = lambda entry: entry.get_comparison())

        # page done


    def add_genarated_entry(self, e):
        entry = Entry(self.cal.get_next_entry(), {'question': e.question, 'answer': e.answer})
        self.entries.append(entry)


    def add_submitted_entry(self, e):
        # tell calendar you've updated
        cal.add_entry(e.datetime)

        # make an entry
        entry = Entry(e.datetime, {'question': e.question, 'answer': e.answer})

        # add the entry
        self.entries.append(entry)

    def genarate(self, num, metadata):

        genarated = table_genarated(metadata)
        s = select([submitted]).order_by(func.random()).limit(num)
        return connection.execute(s)

    def get_entries(self):
        return self.entries

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
