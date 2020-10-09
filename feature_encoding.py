import nltk 
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import pickle


#Encodes the words into onehot feature
def onehot_encoding(words,labels,docs_x,docs_y):
	training =[]
	output = []

	out_empty = [0 for _ in range(len(labels))]
	print (words)
	for x,doc in enumerate(docs_x):
		bag = []
		doc = doc.split()
		wrds = [stemmer.stem(w) for w in doc if w not in "?"]
		for w in words:
			if w in wrds:
				bag.append(1)
			else: 
				bag.append(0) 

		output_row = out_empty[:]
		output_row[labels.index(docs_y[x])] = 1
		

		training.append(bag)
		output.append(output_row)
	
	with open("data.pickle", "wb") as f:
		pickle.dump((words, labels, training, output), f)

	return training, output 