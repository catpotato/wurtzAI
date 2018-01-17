def get_letters(data):

    if type(data) is str:
        intermed = data

    else:
        intermed = list(data)

    result = ''.join(i for i in data if ord(i)<128 and str.isalpha(i))
    return ''.join(sorted(result))
