from keras.models import load_model
from ..transform import get_df
from timer import Timer
import generators
from glob import glob
import random

MAX_LEN = 200
NUM_SAMPLES = 5

def assemble_answers(num, real, temp=0, name=None):
    real_as = assemble_real_bills(num)
    if real:
        return real_qs
    else:
        return assemble_fake(name, real_qs, num, temp, stop_char = '?')

def assemble_questions(num, real, temp=0, name=None):
    real_qs = assemble_real_questions(num)
    if real:
        return real_qs
    else:
        return assemble_fake(name, real_qs, num, temp, stop_char = '?')

def assemble_real_questions(num):
    t = Timer('assembling real questions')
    d = get_df('../raw_data', size=num, max_len=MAX_LEN)['question'].tolist()
    t.stop()
    return d

def assemble_real_bill(num):
    t = Timer('assembling real bills')
    d = get_df('../raw_data', size=num, max_len=MAX_LEN)['answer'].tolist()
    t.stop()
    return d

def assemble_fake(name, real_data, num, temp, stop_char):

    t0 = Timer('assembling fake data for ' + name)

    t = Timer('loading models into memory')

    root_dir = 'models/' + name

    network = glob(root_dir + '/*.h5')[0]
    model = load_model(network)

    with open(root_dir + '/char_labels.pkl', 'rb') as f:
        char_labels = pickle.load(f)

    with open(root_dir + '/labels_char.pkl', 'rb') as f:
        labels_char = pickle.load(f)

    t.stop()

    t = Timer('generating fake data')
    generated_data= []

    for datum in data:
        generated_data.append(generators.generate_rnn(model, char_labels, labels_char, temp = temp, seed = datum, stop_char = stop_char))

    t.stop()

    t0.stop

    return generated_data

def assemble_seq2seq(questions, num):

    t = Timer('loading seq2seq model')

    files = glob('models/s2s/*.pkl')
    recovery = {}

    for item in recovery:
        title = item.replace('.pkl', '').replace('models/', '')
        with open(item) as f:
            data = pickle.load(f)
        recovery[title] = data

    encoder_model.save('models/s2s/s2s_encoder.h5')
    decoder_model.save('models/s2s/s2s_decoder.h5')

    recovery['encoder_model'] = load_model('models/s2s/s2s_encoder.h5')
    recovery['decoder_model'] = load_model('models/s2s/s2s_decoder.h5')

    t.stop()

    t = Timer('genarating seq2seq data')

    answers = []

    for question in questions:
        answers.append(generators.generate_seq2seq(question, recovery_dict))

    t.stop()

    return answers


def examine_line_of_questions(num, temp_range):

    t = Timer('assembling stock rnn bill answers')

    # get a random question
    real_qs = assemble_questions(num, real=True)

    # get a genarated question, at various temperatures
    gen_q_list = [assemble_questions(num, real=False, temp) for temp in temp_range]

    # make them go into the machine
    real_as = [assemble_fake('rnn_stock', real_qs, num, temp, stop_char = '.') for temp in temp_range]

    # put the genarated ones in the machine!
    gen_as = [[]]
    for gen_qs in gen_q_list:
        l = []
        for temp in temp_range:
            l.append(assemble_fake('rnn_stock', gen_qs, num, temp, stop_char = '.') for temp in temp_range)

        gen_as.append(l)


def examine_bill_question(num, temp_range):

    t = Timer('assembling bill and question_net questions')

    # get a random question
    real_qs = assemble_questions(num, real=True)

    # get a genarated question, at various temperatures
    gen_qs = [assemble_questions(num, real=False, temp) for temp in temp_range]

    # get a random answer
    gen_as = [assemble_answers(num, real=False, temp) for temp in temp_range]

    t.stop()

    with open('results/bill_question.txt', 'wb') as f:

        f.write('real questions\n')
        for q in random.sample(real_qs, NUM_SAMPLES):
            f.write(q + '\n')

        f.write('genarated questions\n')
        for l, temp in zip( gen_as, temp_range)
            f.write('temperature ' + temp + '\n')
            for q in random.sample(l, NUM_SAMPLES):
                f.write(q + '\n')

        f.write('genarated questions\n')
        for l, temp in zip( gen_as, temp_range)
            f.write('temperature ' + temp + '\n')
            for a in random.sample(l, NUM_SAMPLES):
                f.write(a + '\n')


    return # ????


def examine_seq2seq(num):

    # get a random question
    real_qs = assemble_questions(num, real=True)

    # get a genarated question, at various temperatures
    gen_qs = [assemble_questions(num, real=False, temp) for temp in temp_range]

    real_as = assemble_seq2seq(real_qs, num)

    gen_as = [assemble_seq2seq(gen_q, num) for gen_q in gen_qs]


def sample_dicts(name, dicts):

    with open('results/' + name, 'wb') as f:









if __name__ == '__main__':
    amount = 700
    # sample a bit from each
    examine_bill_question(amount)
    examine_line_of_questions(amount)
    examine_seq2seq(amount)
