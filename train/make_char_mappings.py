from transform import get_them_and_bill_text, get_big_long_line, transform
import pickle

def save_as(c, name):
    f = open(name + '.pkl', 'wb+')
    print(c)
    pickle.dump(c, f, -1)
    f.close()

def save_as_chars(s, name):
    save_as(list(set(s)), 'char_mappings')


def make_them_and_bill_mappings():
    them, bill = get_them_and_bill_text('raw_data',size=10000)

    save_as_chars(them, 'question_map')
    save_as_chars(bill, 'bill_map')


def make_stock_rnn_mappings():
    line = get_big_long_line(path_to_data, size=10000)
    save_as_chars(line, 'rnn_stock')

if __name__ == '__main__':
    make_them_and_bill_mappings()
    make_stock_rnn_mappings()
    make_seq2seq_mappings()
