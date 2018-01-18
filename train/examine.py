from keras.models import load_model
from transform import get_df
from timer import Timer
from glob import glob
import random, pickle, os, generators
from debuggers import get_letters


MAX_LEN = 200
NUM_SAMPLES = 10
models = {}
def load_models():
    t0 = Timer('loading models into memory')
    for network in glob('models/**/*.h5', recursive=True):
        name = os.path.splitext(os.path.basename(network))[0]
        t = Timer('loading ' + name + ' at ' + network + ' into memory')
        if name == 'question_net':
            models[name] = load_model(network)
        t.stop()

    t0.stop()



def assemble_answers(num, real, real_qs, temp=0, name=None):
    real_as = assemble_real_bill(num)
    if real:
        return real_qs
    else:
        return assemble_fake(name, real_qs, num, temp, stop_char = '?')

def assemble_questions(num, real, temp=0, name=None):
    print('temp: ' + str(temp))
    real_qs = assemble_real_questions(num)
    if real:
        return real_qs
    else:
        return assemble_fake('question_net', real_qs, num, temp, '?')

def assemble_real_questions(num):
    print("number " + str(num))
    t = Timer('assembling real questions')
    d = get_df('raw_data', size=num, max_len=MAX_LEN)['question'].tolist()
    t.stop()
    return d

def assemble_real_bill(num):
    t = Timer('assembling real bills')
    d = get_df('../raw_data', size=num, max_len=MAX_LEN)['answer'].tolist()
    t.stop()
    return d

def assemble_fake(name, real_data, num, temp, stop_char):

    t0 = Timer('assembling fake data for ' + name)

    t = Timer('loading goodies')

    root_dir = 'models/' + name

    model = models[name]

    with open(root_dir + '/char_labels.pkl', 'rb') as f:
        char_labels = pickle.load(f)

    with open(root_dir + '/labels_char.pkl', 'rb') as f:
        labels_char = pickle.load(f)

    t.stop()

    t = Timer('generating fake data')
    generated_data= []

    for datum in real_data:
        generated_data.append(generators.generate_rnn(model, char_labels, labels_char, temp = temp, seed = datum, stop_char = stop_char))

    t.stop()

    t0.stop

    return generated_data

def assemble_seq2seq(questions, num):

    t = Timer('loading seq2seq model')

    files = glob('models/s2s/*.pkl')
    recovery = {}

    for item in files:
        title = os.path.splitext(os.path.basename(item))[0]
        with open(item, 'rb+') as f:
            data = pickle.load(f)
        recovery[title] = data

    recovery['encoder_model'] = models['s2s_encoder']
    recovery['decoder_model'] = models['s2s_decoder']

    t.stop()

    t = Timer('genarating seq2seq data')

    answers = []

    for question in questions:
        answers.append(generators.generate_seq2seq(question, recovery))

    t.stop()

    return answers


def examine_line_of_questions(num, temp_range):

    t = Timer('assembling stock rnn bill answers')

    # get a random question
    real_qs = assemble_questions(num, real=True)

    # get a genarated question, at various temperatures
    # gen_q_list = [assemble_questions(num, real=False, temp=temp) for temp in temp_range]

    # make them go into the machine
    real_as = [assemble_fake('rnn_stock', real_qs, num, temp, stop_char = '.') for temp in temp_range]

    # put the genarated ones in the machine!
    # gen_as = [[]]
    '''for gen_qs in gen_q_list:
        l = []
        for temp in temp_range:
            l.append(assemble_fake('rnn_stock', gen_qs, num, temp, stop_char = '.'))

        gen_as.append(l)'''

    with open('results/rnn_stock.txt', 'w+') as f:

        f.write('responding to real questions')
        for real_a_temp_range, temp in zip(real_as, temp_range):
            f.write('temp: ' + str(temp) + '\n')
            add_qandas(f, real_qs, real_a_temp_range)

        '''f.write('responding to fake questions')
        for gen_qs, gen_a_temp_range, temp in zip(gen_q_list, gen_as, temp_range):
            f.write('question temp: ' + str(temp) + '\n')
            for gen_a_list, temp in zip(gen_a_temp_range, temp_range):
                f.write('answer temp: ' + str(temp) + '\n')
                add_qandas(f, gen_qs, gen_a_list)'''



    t.stop()


def examine_bill(num, temp_range):

    t = Timer('assembling bill and question_net questions')

    # get a random question
    real_qs = assemble_questions(num, real=True)

    # get a genarated question, at various temperatures
    # gen_qs = [assemble_questions(num, real=False, temp=temp) for temp in temp_range]

    # get a random answer
    real_as = [assemble_fake('bill_net', real_qs, num, temp, stop_char = '.') for temp in temp_range]

    with open('results/bill_net.txt', 'w+') as f:

        f.write('responding to real questions\n')
        for temp, real_as_list in zip(temp_range, real_as):
            f.write('temp: ' + str(temp) + '\n')
            add_qandas(f, real_qs, real_as_list)

        '''f.write('responding to fake questions\n')
        for gen_q_list, gen_a_list, temp in zip(gen_qs, temp_range):
            f.write('temp: ' + str(temp) + '\n')
            add_qandas(f, gen_q_list, gen_a_list)'''



    t.stop()



def examine_seq2seq(num, temp_range):

    t = Timer('assembling seq2seq questions')

    # get a random question
    real_qs = assemble_questions(num, real=True)

    # get a genarated question, at various temperatures
    gen_qs = [assemble_questions(num, real=False, temp=temp) for temp in temp_range]

    print(gen_qs)

    real_as = assemble_seq2seq(real_qs, num)

    gen_as = [assemble_seq2seq(gen_q, num) for gen_q in gen_qs]

    with open('results/seq2seq.txt', 'w+') as f:

        f.write('responding to real questions\n')
        add_qandas(f, real_qs, real_as)

        f.write('responding to fake questions\n')
        for l, temp in zip(gen_as, temp_range):
            f.write('temp: ' + str(temp) + '\n')
            add_qandas(f, gen_qs, l)

    t.stop()



def add_list(f, l):
    if len(l) >= NUM_SAMPLES:
        for item in random.sample(l, NUM_SAMPLES):
            f.write(item + '\n')

def add_qandas(f, qs, ans):
    for q,a in zip(qs, ans):
        f.write(q + ' ' + a + '\n')


if __name__ == '__main__':

    load_models()
    amount = 10
    # examine_seq2seq(amount, [(i+1)*.1 for i in range(10)])
    # examine_bill(amount, [(i+1)*.1 for i in range(10)])
    # examine_line_of_questions(amount, [(i+1)*.1 for i in range(10)])

    gen_qs = [assemble_questions(amount, real=False, temp=temp+1/10) for temp in range(10)]
