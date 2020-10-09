import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD



def train_model(training, output):
	X_train = np.array(training)
	y_train = np.array(output)

	input_layer_shape = (len(X_train[0]),)
	output_layer_shape = len(y_train[0])

	model = Sequential()
	model.add(Dense(256, input_shape=(len(X_train[0]),), activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(128, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(output_layer_shape, activation='softmax'))

	sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

	hist = model.fit(X_train, y_train, epochs=200, batch_size=5, verbose=1)
	model.save('chatbot_model.h5', hist)
	
	print("model created")
	return model