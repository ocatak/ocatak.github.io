# Load LSTM network and generate text
import sys
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import io
import random

# load ascii text and covert to lowercase
# filename = "E.T.A._HOFFMANN-Ugursuz-Miras - tr.txt"
filename = "rockyou_simple.txt"
#raw_text = open(filename).read()

with io.open(filename,'r',encoding='utf8') as f:
    raw_text = f.read()

raw_text = raw_text.replace("\r", " ").replace("\n"," ")[0:50000]
#raw_text = raw_text.lower()
# create mapping of unique chars to integers, and a reverse mapping
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)
print( "Total Characters: ", n_chars)
print( "Total Vocab: ", n_vocab)
# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
    seq_in = raw_text[i:i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print( "Total Patterns: ", n_patterns)
# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)

# define the LSTM model
model = Sequential()
model.add(LSTM(128, input_shape=(X.shape[1], X.shape[2]), activation='tanh', return_sequences=True))
model.add(Dropout(0.1))
model.add(LSTM(128, activation='tanh'))
model.add(Dropout(0.1))
model.add(Dense(y.shape[1], activation='softmax'))

# load the network weights
filename = "01-rockyou.hdf5"

model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

for i in range(100):
    # pick a random seed
    start = numpy.random.randint(0, len(dataX)-1)
    pattern = dataX[start]
    
    space_idx = random.choice([pos for pos, char in enumerate(raw_text) if char == " "])
    pattern = dataX[space_idx]
    #print(pattern,type(pattern))
    #pattern = "ferhatozgu"
    #pattern = list([char_to_int[a] for a in pattern])
    print( "Seed:")
    print( "\"", ''.join([int_to_char[value] for value in pattern]), "\"")
    # generate characters
    sys.stdout.write("-")
    for i in range(100):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        result = int_to_char[index]
        seq_in = [int_to_char[value] for value in pattern]
        sys.stdout.write(result)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
    sys.stdout.write("-")
    print( "\nDone.")
