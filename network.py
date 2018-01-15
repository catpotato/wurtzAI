import numpy as np
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation, Dropout
from dbmodel import table_submitted, table_genarated
import datetime

class Network:
    def __init__(self, name):
        self.name = name
        self.model = model.load('train/' + name)

    def generate_qa_pairs(self, amount):
        # TODO genarate questions from model
        pass

    def genarate_answer(self, question):
        # TODO make answers from a given question from the model
        pass

    def add_question(self, question):
        engine = create_engine('sqlite:///data.db', echo=True)
        metadata = MetaData()

        submitted = table_submitted(metadata)

        ins = submitted.insert()
        data = [{
            'month':datetime.datetime.now(),
            'datetime':datetime.datetime.now(),
            'question':question,
            'answer':genarate_answer(question)
        }]

        connection.execute(ins, data)


    def generate_db(self):
        engine = create_engine('sqlite:///data.db', echo=True)
        metadata = MetaData()

        generated = table_genarated(metadata)

        datum = []

        ins = generated.insert()

        for question, answer in zip(generate_qa_pairs(10000)):
            data = {
                'question':question,
                'answer':answer
            }
            datum.append(data)

        connection.execute(ins, datum)
