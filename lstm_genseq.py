from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM

import pandas as pd
from random import randint
import numpy as np
import time

# settings
maxlen = 64
step = 1
input_dim = 1
output_dim = 1

# helper fn
def loadData(fName):
	D = np.genfromtxt(fName, delimiter=',')
	rawX = []
	rawY = []
	for i in range(0, len(D) - maxlen, step):
		rawX.append(D[i: i + maxlen, 0])
		rawY.append(D[i + maxlen, 1])

	X = np.zeros((len(rawX), maxlen, input_dim), dtype=np.float64)
	Y = np.zeros((len(rawY), output_dim), dtype=np.bool)

	for i, seq in enumerate(rawX):
		X[i, :, 0] = rawX[i]
		Y[i, 0] = rawY[i]

	return (X,Y)


print "Loading data"
# read data
(Xtrn, Ytrn) = loadData('genseq_trn.csv');
(Xtst, Ytst) = loadData('genseq_tst.csv');


print "Setting up model"
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, input_dim), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(output_dim))
model.add(Activation("softmax"))
model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

print "Start training"
# and now train the model
# batch_size should be appropriate to your memory size
# number of epochs should be higher for real world problems
try:
	trainTime = 0
	for iteration in range(1, 60):
		print('-' * 50)
		print('Iteration', iteration)

		start = int(round(time.time() * 1000))
		model.fit(Xtrn, Ytrn, nb_epoch=1, validation_split=0.2)
		finish = int(round(time.time() * 1000))
		trainTime += finish - start;

		print "Predicting..."
		Ypred = model.predict(Xtst)
		np.savetxt("pred" + str(iteration), Ypred, delimiter=",")

except KeyboardInterrupt:
	print "\ninterrupted fitting model, done."

print "Total training time %d ms" % trainTime
print "Saving model..."
json_string = model.to_json()
open('lstm_genseq_architecture.json', 'w').write(json_string)
model.save_weights('lstm_genseq_weights.h5')
print "Done."
