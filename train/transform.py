import sys
sys.path.append("..")

from glob import glob
from helpers import get_csv_as_dict, merge_dictionaries
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split


'''

    these folks just give you back a df or dict of the bill wurtz data

'''

def get_df(path_to_data, size=False):

    csvs = glob("../" + path_to_data + "/*/*.csv")

    questions_and_answers = pd.DataFrame(columns=['question', 'answer'])

    for csv in csvs:
        questions_and_answers = pd.concat([questions_and_answers, pd.read_csv(csv)], ignore_index=True)

    if size:
        questions_and_answers.sample(frac=(size/questions_and_answers.shape[0])).reset_index(drop=True)

    return questions_and_answers

def get_dict(path_to_data):

    csvs = glob("../" + path_to_data + "/*/*.csv")

    questions_and_answers = merge_dictionaries([get_csv_as_dict(csv) for csv in csvs])
    questions, answers = merge_keys_and_values(questions_and_answers)

    return questions_and_answers


'''

makes a big long line of questions

e.g.

"do you like stuff? yeah i like stuff. do you like shit? yeah i like shit. is there a reason to be scared? yeah there is a reason to be scared."

'''

def get_big_long_line(path_to_data, size=False):

    questions_and_answers = get_df(path_to_data)
    questions_and_answers["qanda"] =  questions_and_answers["question"] + questions_and_answers["answer"]
    big_long_line = questions_and_answers["qanda"].str.cat(sep = '')

    return big_long_line

def transform(path_to_data, size=False, train_size=False, max_size=100):

    questions_and_answers = get_df(path_to_data, size=size)

    # funky transforms, start char is \t, end char is \n
    questions_and_answers['question'] = '\t' + questions_and_answers['question'].astype(str) +'\n'
    questions_and_answers['answer'] = '\t' + questions_and_answers['answer'].astype(str) +'\n'

    dataframe["final"] = dataframe["question"] + '\t'+ dataframe["answer"]

    # TODO maybe drop all of the ones that are too long

    # LEFTOFF
    # Trying to remove really long ones

    #questions_and_answers = questions_and_answers.loc[questions_and_answers['answer'] == "yes."]
    #questions_and_answers = questions_and_answers.loc[len(questions_and_answers['answer']) <= max_size]


    if(train_size):
        train, test = train_test_split(questions_and_answers, train_size=train_size)
    else:
        train = questions_and_answers
        test = None

    return train, test

if __name__ == "__main__":
    get_big_long_line('raw_data')
