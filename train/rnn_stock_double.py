from transform import get_big_long_line
import random
import numpy as np
from glob import glob
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation, Dropout

if __name__ == "__main__":

    import os

    

    # get a list of the unique chars
    chars = list(set(text))

    # how big the window looking back is
    max_len = 20

    #?????
    model = Sequential()
    model.add(LSTM(512, return_sequences=True, input_shape=(max_len, len(chars))))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(len(chars)))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    # samples every 3 characters and goes through and makes a list of every 3 chars with the window size
    step = 3
    inputs = []
    outputs = []
    for i in range(0, len(text) - max_len, step):
        inputs.append(text[i:i+max_len])
        outputs.append(text[i+max_len])

    # get a obverse and inverse labeling for each char
    char_labels = {ch:i for i, ch in enumerate(chars)}
    labels_char = {i:ch for i, ch in enumerate(chars)}

    # using bool to reduce memory usage, make zeros, x is 2-d array of one-hot vectors
    # ie
    # y is single char

    '''
    example = 'cab dab'
    example_char_labels = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        ' ' : 4
    }
    x
    [   a   b  c  d  ' '
        [0, 0, 1, 0, 0], # c
        [1, 0, 0, 0, 0], # a
        [0, 1, 0, 0, 0], # b
        [0, 0, 0, 0, 1], # (space)
        [0, 0, 0, 1, 0], # d
        [1, 0, 0, 0, 0], # a
        [0, 1, 0, 0, 0]  # b
    ]
    y
    [[0, 0, 0, 0, 1]]
    '''


    X = np.zeros((len(inputs), max_len, len(chars)), dtype=np.bool)
    y = np.zeros((len(inputs), len(chars)), dtype=np.bool)



    # set the appropriate indices to 1 in each one-hot vector
    for i, example in enumerate(inputs):
        for t, char in enumerate(example):
            X[i, t, char_labels[char]] = 1
        y[i, char_labels[outputs[i]]] = 1


    # probably not worth understanding

    def generate(temperature=0.35, seed=None, num_chars=100):
        predicate=lambda x: len(x) < num_chars

        if seed is not None and len(seed) < max_len:
            raise Exception('Seed text must be at least {} chars long'.format(max_len))

        # if no seed text is specified, randomly select a chunk of text
        else:
            start_idx = random.randint(0, len(text) - max_len - 1)
            seed = text[start_idx:start_idx + max_len]

        sentence = seed
        generated = sentence

        while predicate(generated):
            # generate the input tensor
            # from the last max_len characters generated so far
            x = np.zeros((1, max_len, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_labels[char]] = 1.

            # this produces a probability distribution over characters
            probs = model.predict(x, verbose=0)[0]

            # sample the character to use based on the predicted probabilities
            next_idx = sample(probs, temperature)
            next_char = labels_char[next_idx]

            generated += next_char
            sentence = sentence[1:] + next_char
        return generated

    def sample(probs, temperature):
        """samples an index from a vector of probabilities
        (this is not the most efficient way but is more robust)"""
        a = np.log(probs)/temperature
        dist = np.exp(a)/np.sum(np.exp(a))
        choices = range(len(probs))
        return np.random.choice(choices, p=dist)


    # the real deal
    epochs = 10
    for i in range(epochs):
        print('epoch %d'%i)

        # set nb_epoch to 1 since we're iterating manually
        # comment this out if you just want to generate text
        model.fit(X, y, batch_size=128, epochs=1)

        # preview
        for temp in [0.2, 0.5, 1., 1.2]:
            print('temperature: %0.2f'%temp)
            print('%s'%generate(temperature=temp))

    model.save('rnn_double.h5')
