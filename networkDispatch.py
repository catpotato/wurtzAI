from keras.models import load_model
from dbmodel import table_person, table_trying_to_be_a_person, table_submitted
import datetime
import os
import pickle
from glob import glob
from sqlalchemy import create_engine, MetaData
from train.generators import generate_seq2seq_recovery, generate_rnn_recovery
from train.transform import get_df
from tqdm import tqdm
from keras.backend import clear_session


'''

IMPORTANT: this guy must stay loaded the whole time!!
it contains all the networks in it and does all of the heavy lifting fro handling keeping things in memory and such

'''



class NetworkDispatch:
    ''' this guy makes new things when you enter something in the filed or are generating stuff '''
    def __init__(self):
        self.models = {}
        self.recovery = {}
        self.load_models()
        self.generate_recoveries()
        self.styles = ['good', 'fine', 'ok', 'wow']


    '''

        the load functions at the top load in all the data they can find and these functions down here take that data and pipe it correctly into the functions

        each model has its own `recovery` which is just its pickles stored in a states_value

        the s2s's fight over their encoders because oh well

    '''

    def gen_good(self, question):
        # seq2seq Network
        models = {}
        models['encoder'] = self.models['s2s_encoder']
        models['decoder'] = self.models['s2s_decoder']
        recovery = self.recovery['s2s']
        return generate_seq2seq_recovery(question, models, recovery)

    def gen_fine(self, question):
        # rnn with temperature .15
        model = self.models['rnn_stock']
        recovery = self.recovery['rnn_stock']
        char_labels = recovery
        stop_char = '.'
        temp = .15
        return generate_rnn_recovery(question, model, recovery, stop_char, temp)


    def gen_ok(self, question):
        # rnn with temperature .35
        model = self.models['rnn_stock']
        recovery = self.recovery['rnn_stock']
        stop_char = '.'
        temp = .35
        return generate_rnn_recovery(question, model, recovery, stop_char, temp)

    def gen_wow(self, question):
        # rnn with temperature .35
        model = self.models['bill_net']
        recovery = self.recovery['bill_net']
        stop_char = '.'
        temp = .1
        return generate_rnn_recovery(question, model, recovery, stop_char, temp)

        def add_question(self, question):
            engine = create_engine('sqlite:///data.db', echo=True)
            connection = engine.connect()
            metadata = MetaData()

            submitted = table_submitted(metadata)

            ins = submitted.insert()
            data = [{
                'month': datetime.datetime.now(),
                'datetime': datetime.datetime.now(),
                'question': question,
                'good': self.gen_good(question),
                'fine': self.gen_fine(question),
                'ok': self.gen_ok(question),
                'wow': self.gen_wow(question)
            }]

            connection.execute(ins, data)

    def gen_answer(self, style, question):
        # meat and potatoes
        if style == 'good':
            return self.gen_good(question)

        elif style == 'fine':
            return self.gen_fine(question)

        elif style == 'ok':
            return self.gen_ok(question)

        elif style == 'wow':
            return self.gen_wow(question)

    def load_models(self):
        print ('loading models')
        clear_session()

        models = {}

        for network in glob('train/models/**/*.h5', recursive=True):
            name = os.path.splitext(os.path.basename(network))[0]
            print ('loading ' + name + ' from ' + network)
            models[name] = load_model(network)
            print('done')

        self.models = models


    def generate_recoveries(self):

        print('generating recoveries')
        # walk all directories, so that you get a dict formatted like dict['bill_net']['char_labels'] to get char labels
        networks = os.walk('train/models')

        recovery = {}

        for network in networks:
            net_name = os.path.basename(network[0])

            # load each pickled file
            pickles = glob('train/models/' + net_name + '/*.pkl')
            network_data = {}
            for pick in pickles:


                # get pickle name
                filename = os.path.splitext(os.path.basename(pick))[0]

                with open(pick, 'rb+') as f:
                    # add to dict
                    data = pickle.load(f)
                    network_data[filename] = data

            print(net_name)
            recovery[net_name] = network_data


        self.recovery = recovery

    def get_answers(self, questions):

        print('generating answers')

        data = {}

        for question in tqdm(questions):
            data['question'] = question
            for style in self.styles:
                data[style] = self.gen_answer(style, question)

        return data

    def gen_fake_q(self, answer):
        # seq2seq Network
        models = {}
        models['encoder'] = self.models['s2s_questions_encoder']
        models['decoder'] = self.models['s2s_questions_decoder']
        recovery = self.recovery['s2s_questions']
        return generate_seq2seq_recovery(answer, models, recovery)

    def generate_db(self, num=1000):

        # get questions
        real_qs = get_df('raw_data', size=num)['question'].tolist()
        fake_qs = [self.gen_fake_q(answer) for answer in tqdm(get_df('raw_data', size=num)['answer'].tolist())]

        # get answers to those questions
        real_answers = self.get_answers(real_qs)
        fake_answers = self.get_answers(fake_qs)

        engine = create_engine('sqlite:///data.db', echo=True)
        connection = engine.connect()
        metadata = MetaData()

        # real

        person = table_person(metadata)
        ins = person.insert()

        connection.execute(ins, real_answers)

        # fake

        trying_to_be_a_person = table_trying_to_be_a_person(metadata)
        ins = trying_to_be_a_person.insert()

        connection.execute(ins, fake_answers)

if __name__ == '__main__':
    nd = NetworkDispatch()
    nd.generate_db()
