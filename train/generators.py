MAX_TEST_RUN = 1000


def generate_seq2seq(text, recovery_dict):
    '''

    encoder_model,
    decoder_model,
    num_encoder_tokens,
    num_decoder_tokens,
    target_token_index,
    max_decoder_seq_length,
    input_token_index

    '''

    # recovery
    encoder_model = recovery_dict['encoder_model']
    decoder_model = recovery_dict['decoder_model']
    num_encoder_tokens = recovery_dict['num_encoder_tokens']
    num_decoder_tokens = recovery_dict['num_decoder_tokens']
    target_token_index = recovery_dict['target_token_index']
    max_decoder_seq_length = recovery_dict['max_decoder_seq_length']
    input_token_index = recovery_dict['input_token_index']



    # convert text into input sequence

    input_seq = np.zeros(len(text), num_encoder_tokens)

    for i, char in enumerate(text):
        input_seq[i, input_token_index[char]] = 1.

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


def generate_rnn(model, char_labels, labels_char, temperature=0.35, seed=None, stop_char):

    test_range = 1000

    not_q=lambda x: x[-1] != stop_char

    if seed:
        genarated = ''
        sentence = seed
        while not_q(generated):
            x = np.zeros((1, test_range, len(char_labels)))
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

    else:
        return stop_char
