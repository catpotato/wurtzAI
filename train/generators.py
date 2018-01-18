import numpy as np
import math, random
MAX_TEST_RUN = 1000


def generate_seq2seq_recovery(text, models, recovery):
    recovery['encoder_model'] = models['encoder']
    recovery['decoder_model'] = models['decoder']
    generate_seq2seq(text, recovery)

def generate_seq2seq(text, recovery_dict):
    # prevent nan attacks
    if type(text) is float:
        return 'nice try stephen fry'
    '''

    encoder_model,
    decoder_model,
    num_encoder_tokens,
    num_decoder_tokens,
    target_token_index,
    max_decoder_seq_length,
    input_token_index

    '''

        # recovery : hack here to get things working => nums are lengths of their arrays
    encoder_model = recovery_dict['encoder_model']
    decoder_model = recovery_dict['decoder_model']
    target_token_index = recovery_dict['target_token_index']
    input_token_index = recovery_dict['input_token_index']
    num_encoder_tokens = len(input_token_index)
    num_decoder_tokens = len(target_token_index)
    max_decoder_seq_length = int(recovery_dict['max_decoder_seq_length'])

    reverse_input_char_index = dict((i, char) for char, i in input_token_index.items())
    reverse_target_char_index = dict((i, char) for char, i in target_token_index.items())



    # convert text into input sequence

    input_seq = np.zeros((1, len(text), num_encoder_tokens))

    for i, char in enumerate(text):
        try:
            input_seq[0, i, input_token_index[char]] = 1.
        except KeyError:
            input_seq[0, i, input_token_index[' ']] = 1.



    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0, target_token_index['\t']] = 1.

    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value)

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char

        # Exit condition: either hit max length
        # or find stop character.
        if (sampled_char == '\n' or
           len(decoded_sentence) > max_decoder_seq_length):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.

        # Update states
        states_value = [h, c]

    return decoded_sentence

def generate_rnn_recovery(question, model, recovery, stop_char, temp):

    char_labels = recovery['char_labels']
    labels_char = recovery['labels_char']

    return generate_rnn(model=model, char_labels=char_labels, labels_char=labels_char, stop_char=stop_char, temp=temp, seed=question)


def generate_rnn(model, char_labels, labels_char, stop_char, temp=0.35, seed=None):

    # checks to make sure that the seed is long enough, could use some improvement

    while len(seed) < 20:
        seed = seed + seed

    seed = seed[-20:]

    return(generate_stock(model=model, char_labels=char_labels, labels_char=labels_char, temperature=temp, seed=seed, stop_char=stop_char))

def sample(probs, temperature):
    """samples an index from a vector of probabilities
    (this is not the most efficient way but is more robust)"""
    a = np.log(probs)/temperature
    dist = np.exp(a)/np.sum(np.exp(a))
    choices = range(len(probs))
    return np.random.choice(choices, p=dist)

def generate_stock(model, char_labels, labels_char, temperature=0.35, seed=None, stop_char='?', num_chars=100):

    max_len = 20
    predicate=lambda x: x[-1] != stop_char

    if seed is not None and len(seed) < max_len:
        raise Exception('Seed text must be at least {} chars long'.format(max_len))

    sentence = seed
    generated = ' '

    while predicate(generated):
        # generate the input tensor
        # from the last max_len characters generated so far
        x = np.zeros((1, max_len, len(char_labels)))
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
