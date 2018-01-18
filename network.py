from keras.models import Sequential, load_model
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation, Dropout
import glob

class Network:
    def __init__(self, kind, directory):

        self.full_path = 'train/models/' + directory
        self.kind = kind
        if kind == 's2s':

            self.encoder = load_model(glob.glob(self.full_path + '/*encoder.h5')[0])
            self.decoder = load_model(glob.glob(self.full_path + '/*decoder.h5')[0])

        elif kind == 'rnn':

            self.model = load_model(glob.glob(self.full_path + '/*.h5')[0])

        self.recover()

        def recover(self):


            # load each pickled file
            pickles = glob(self.full_path + '/*.pkl')
            for pickle in pickles

                # get pickle name
                filename = os.path.splitext(os.path.basename(pickle))[0]

                with open(pickle, 'rb+') as f:
                    # add to dict
                    data = pickle.load(f)
                    recovery[filename] = data

        self.recovery = recovery
