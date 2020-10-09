import nltk 
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import random 
import json 
import pickle

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

from keras.models import load_model

###############################learn this 
with open("intents.json") as file: 
	data = json.load(file)
##############################
try:
	with open("data.pickle", "rb") as f:
		words, labels, training, output = pickle.load(f)
	error


except:
	words = []
	labels = []
	docs_x = []
	docs_y = []
	for intent in data["intents"]:
		for pattern in intent["patterns"]:
			wrds = nltk.word_tokenize(pattern)
			words.extend(wrds)
			docs_x.append(pattern)
			docs_y.append(intent["tag"])
	###############################learn this
		if intent["tag"] not in labels:
			labels.append(intent["tag"])
	###############################
	words =[stemmer.stem(w.lower()) for w in words]
	words = sorted(list(set(words)))

	labels = sorted(labels)


	training =[]
	output = []

	out_empty = [0 for _ in range(len(labels))]
	print (words)
	for x,doc in enumerate(docs_x):
		
		bag = []
		doc = doc.split()
		wrds = [stemmer.stem(w) for w in doc if w not in "?"]
		print (wrds)
		for w in words:
			if w in wrds:
				bag.append(1)
				# print ("ok")
			else: 
				bag.append(0)
				# print ("ok") 

		output_row = out_empty[:]
		output_row[labels.index(docs_y[x])] = 1
		

		training.append(bag)
		output.append(output_row)

	with open("data.pickle", "wb") as f:
		pickle.dump((words, labels, training, output), f)




X_train = np.array(training)
y_train = np.array(output)

input_layer_shape = (len(X_train[0]),)
output_layer_shape = len(y_train[0])
print (X_train.shape)
print (X_train[5])
print (X_train[6])
print (X_train[7])

model = Sequential()
model.add(Dense(128, input_shape=(len(X_train[0]),), activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(output_layer_shape, activation='softmax'))


# model = load_model('chatbot_model.h5')
try: 
	model = load_model('chatbot_model.h5')

	

except:
	sgd = SGD(lr=0.01, decay=1e-6, momentum=0.8, nesterov=True)
	model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

	hist = model.fit(X_train, y_train, epochs=100, batch_size=5, verbose=1)
	model.save('chatbot_model.h5', hist)
	
	print("model created")

def bag_of_words(s, words):
	bag = [0 for _ in range(len(words))]
	bag = np.zeros((1,len(bag)))

	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i, w in enumerate(words):
			if w == se:
				bag[0,i] = 1
	# print (bag)
	return bag


def chat():
	print("Hello, you've reached Sisoft Technologies, how can we help you.(type quit to stop)!")
	while True:
		inp = input("You: ")
		if inp.lower() == "quit":
			break



		bag = bag_of_words(inp, words)

		# bag = np.zeros((1,85))
		# bag[0,12] = 1

		results = model.predict(bag)
		results_index = np.argmax(results)
		tag = labels[results_index]

		for tg in data["intents"]:
			if tg['tag'] == tag:
				responses = tg['responses']

		print(random.choice(responses))

# chat()