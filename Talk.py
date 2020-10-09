from extracting_data import extract_data
from feature_encoding import onehot_encoding
from train_model import train_model

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import pickle
import json
import random
from keras.models import load_model
from keras.backend import clear_session



name = ""
query = ""
phone_num = ""

with open("intents.json") as file: 
	data = json.load(file)

def bag_of_words(s, words):
	bag = [0 for _ in range(len(words))]
	bag = np.zeros((1,len(bag)))

	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i, w in enumerate(words):
			if w == se:
				bag[0,i] = 1
	return bag

def ask(inp):
	try:
		model = load_model('chatbot_model.h5')
		bag = bag_of_words(inp, words)
		results = model.predict(bag)
		results_index = np.argmax(results)
		tag = labels[results_index]
		for tg in data["intents"]:
			if tg['tag'] == tag:
				responses = tg['responses']
		return (random.choice(responses))
	except:
		model = reconstruct_model()
		return("p..pp..ppp...Pardon me, I am undergoing some internal repair")
		
		
	


def chat():
	# print("Hello, you've reached Sisoft Technologies, how can we help you.(type quit to stop)!")
	ask_name = 3
	cnt = 0 

	while True:
		cnt +=1
		inp = input("You: ")
		if inp.lower() == "quit":
			break




		# bag = bag_of_words(inp, words)

		

		# results = model.predict(bag)
		# results_index = np.argmax(results)
		# tag = labels[results_index]

		# for tg in data["intents"]:
		# 	if tg['tag'] == tag:
		# 		responses = tg['responses']

		# print(random.choice(responses))
		
		print (ask(inp))
		if cnt ==3:
			question()

def question():
	print ("Ah, Would you mind telling about yourself.")
	while True: 
		inp = input("You: ")
		bag = bag_of_words(inp, words)
		results = model.predict(bag)
		results_index = np.argmax(results)
		tag = labels[results_index]
		
		if tag == "No" or tag == "Yes":
			break
		print ("I am not sure, what you said....")
		print ("Would you mind telling you name")
	if tag == "No":
		print ("No Problem, make sure you are not left with any query.")

	if tag == "Yes":
		name = input("Name: ")
		query = input("Query: ")
		phone_num = input("Phone_Num: ")
		print ("That will be all. Sisoft Technologies will be calling you asap.")

def reconstruct_model():
	words, labels, docs_x, docs_y = extract_data()
	training, output = onehot_encoding(words, labels, docs_x, docs_y)
	model = train_model(training, output)



try:
	with open("data.pickle", "rb") as f:
		words, labels, training, output = pickle.load(f)
except: 
	words, labels, docs_x, docs_y = extract_data()
	training, output = onehot_encoding(words, labels, docs_x, docs_y)

try:
	model = load_model('chatbot_model.h5')

except:
	model = train_model(training, output)

def new_data():
	words, labels, docs_x, docs_y = extract_data()
	training, output = onehot_encoding(words, labels, docs_x, docs_y)
	model  = train_model(training, output)



# new_data()
# chat()
# print (ask("Tell me about your courses"))
# new_data()