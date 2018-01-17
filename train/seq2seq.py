from transform import transform
from keras.models import Model, load_model
from keras.layers import Input, LSTM, Dense
import numpy as np
from make_char_mappings import save_as, load_pickle

def decode_sequence(input_seq):
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

if __name__ == "__main__":
    questions, answers = transform('raw_data')

    # i will probably understand these later

    # [ ]
    batch_size = 64  # Batch size for training.
    # [ ]
    epochs = 100  # Number of epochs to train for.
    # [ ]
    latent_dim = 256  # Latent dimensionality of the encoding space.
    # [x]
    num_samples = 10000  # Number of samples to train on.
    size_lim=100

    # my own code
    train, test = transform("raw_data", size = num_samples, max_size = size_lim)

    # Vectorize the data.
    input_texts = train['question'].tolist()
    target_texts = train['answer'].tolist()

    print("train['question']")
    print(train['question'])

    # makes a set, doesn't repeat, trying to get unique chars
    input_characters = set(''.join(input_texts))
    target_characters = set(''.join(target_texts))

    # just turning it into a list
    input_characters = sorted(list(input_characters))
    target_characters = sorted(list(target_characters))
    # [ ]
    num_encoder_tokens = len(input_characters)
    num_decoder_tokens = len(target_characters)
    # finds how long each of these would have to be at max
    max_encoder_seq_length = max([len(txt) for txt in input_texts])
    max_decoder_seq_length = max([len(txt) for txt in target_texts])

    # just checking in
    print('Number of samples:', len(input_texts))
    print('Number of unique input tokens:', num_encoder_tokens)
    print('Number of unique output tokens:', num_decoder_tokens)
    print('Max sequence length for inputs:', max_encoder_seq_length)
    print('Max sequence length for outputs:', max_decoder_seq_length)

    # turns the list into a dict
    input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
    target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])

    # making empty arrays that are big enough for one hot vectors
    # ie https://github.com/ml4a/ml4a-guides/raw/f31929024c51bdc409b52e91a77725291fa16564/assets/rnn_3tensor.png

    encoder_input_data = np.zeros((len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype='float32')
    decoder_input_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype='float32')
    decoder_target_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype='float32')

    # converting to one-hots, maybe go back and change this

    for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
        for t, char in enumerate(input_text):
            encoder_input_data[i, t, input_token_index[char]] = 1.
        for t, char in enumerate(target_text):
            # decoder_target_data is ahead of decoder_input_data by one timestep
            decoder_input_data[i, t, target_token_index[char]] = 1.
            if t > 0:
                # decoder_target_data will be ahead by one timestep
                # and will not include the start character.
                decoder_target_data[i, t - 1, target_token_index[char]] = 1.

    # Define an input sequence and process it.
    encoder_inputs = Input(shape=(None, num_encoder_tokens))
    encoder = LSTM(latent_dim, return_state=True)
    encoder_outputs, state_h, state_c = encoder(encoder_inputs)
    # We discard `encoder_outputs` and only keep the states.
    encoder_states = [state_h, state_c]

    # Set up the decoder, using `encoder_states` as initial state.
    decoder_inputs = Input(shape=(None, num_decoder_tokens))
    # We set up our decoder to return full output sequences,
    # and to return internal states as well. We don't use the
    # return states in the training model, but we will use them in inference.
    decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
    decoder_dense = Dense(num_decoder_tokens, activation='softmax')
    decoder_outputs = decoder_dense(decoder_outputs)

    # Define the model that will turn
    # `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

    save = False



    # Run training
    if save:

        model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
        model.fit([encoder_input_data, decoder_input_data], decoder_target_data, batch_size=batch_size, epochs=epochs, validation_split=0.2)
        model.save('models/s2s/s2s.h5')
    else:
        model = load_model('models/s2s/s2s.h5')
        print('WARNING THIS WILL NOT BE SAVED!')

    # Next: inference mode (sampling).
    # Here's the drill:
    # 1) encode input and retrieve initial decoder state
    # 2) run one step of decoder with this initial state
    # and a "start of sequence" token as target.
    # Output will be the next target token
    # 3) Repeat with the current target token and current states

    # Define sampling models
    encoder_model = Model(encoder_inputs, encoder_states)

    decoder_state_input_h = Input(shape=(latent_dim,))
    decoder_state_input_c = Input(shape=(latent_dim,))
    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
    decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model = Model( [decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)

    # Reverse-lookup token index to decode sequences back to
    # something readable.
    reverse_input_char_index = dict((i, char) for char, i in input_token_index.items())
    reverse_target_char_index = dict((i, char) for char, i in target_token_index.items())

    if save:
        encoder_model.save('models/s2s/s2s_encoder.h5')
        decoder_model.save('models/s2s/s2s_decoder.h5')
    else:
        encoder_model = load_model('models/s2s/s2s_encoder.h5')
        decoder_model = load_model('models/s2s/s2s_decoder.h5')



    to_save = [
        'num_decoder_tokens',
        'target_token_index',
        'max_decoder_seq_length',
        'num_decoder_tokens',
        'num_encoder_tokens',
        'input_token_index'
    ]





    save_as(num_decoder_tokens, 'models/s2s/')
    save_as(target_token_index, 'models/s2s/target_token_index')
    save_as(max_decoder_seq_length, 'models/s2s/max_decoder_seq_length')
    save_as(num_decoder_tokens, 'models/s2s/num_decoder_tokens')
    save_as(num_encoder_tokens, 'models/s2s/num_encoder_tokens')
    save_as(input_token_index, 'models/s2s/input_token_index')



    for seq_index in range(100):
        # Take one sequence (part of the training test)
        # for trying out decoding.
        input_seq = encoder_input_data[seq_index: seq_index + 1]
        decoded_sentence = decode_sequence(input_seq)
        print('-')
        print('Input sentence:', input_texts[seq_index])
        print('Decoded sentence:', decoded_sentence)
