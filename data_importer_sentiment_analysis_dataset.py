import pickle
import os
import nltk
from nltk.tokenize import word_tokenize
import random
import common_functions


def get_2_lists(path):
	with open(path, 'r', encoding="utf8") as f:
		line = f.readline()
		line = f.readline()  # skips 1st line
		lines = []
		while line:
			if line != ' ':
				split_line = line.split(',')
				score = int(split_line[1])
				text = split_line[3:len(split_line)]
				text = ''.join(text)
				text = text.strip(' ').replace('\n', '')
				lines.append((text, score))
			line = f.readline()

	pos_texts = []
	neg_texts = []
	for item in lines:
		if item[1] == 1:
			pos_texts.append(item[0])
		elif item[1] == 0:
			neg_texts.append(item[0])
		else:
			print("error reading score")
	return pos_texts, neg_texts


def import_and_process(f_name, max_wf):
	currentPath = str(os.path.dirname(os.path.realpath(__file__)))
	rel_folder_path = r'\training_data\\'
	full_path = currentPath + rel_folder_path + f_name
	pos_texts, neg_texts = get_2_lists(full_path)

	print('len_1: ', len(pos_texts))
	pos_texts = pos_texts[:len(neg_texts)]
	print('len_2: ', len(pos_texts))

	all_words = []
	documents = []

	#  j is adject, r is adverb, and v is verb
	allowed_word_types = ["J", "R", "V"]
	# allowed_word_types = ["J"]

	try:
		for p in pos_texts:
			documents.append((p, "pos"))
			words = word_tokenize(p)
			pos = nltk.pos_tag(words)
			for w in pos:
				if w[1][0] in allowed_word_types:
					all_words.append(w[0].lower())
	except(LookupError):
		nltk.download()

	for p in neg_texts:
		documents.append((p, "neg"))
		words = word_tokenize(p)
		pos = nltk.pos_tag(words)
		for w in pos:
			if w[1][0] in allowed_word_types:
				all_words.append(w[0].lower())
	
	random.shuffle(documents)

	all_words = nltk.FreqDist(all_words)
	word_features = list(all_words.keys())[:max_wf]
	return word_features, documents


def process(f_name, min_pos_score, max_word_features=5000):
	# for sentiment analysis csv
	currentPath = str(os.path.dirname(os.path.realpath(__file__)))
	rel_folder_path = r'\Pickles\\'
	pickle_path_doc = currentPath + rel_folder_path + f_name[:-4] + '_doc.pickle'
	pickle_path_wf = currentPath + rel_folder_path + f_name[:-4] + '_wf.pickle'
	if not os.path.isfile(pickle_path_doc) or not os.path.isfile(pickle_path_wf):
		try:
			os.remove(pickle_path_doc)
		except(FileNotFoundError):
			pass
		try:
			os.remove(pickle_path_wf)
		except(FileNotFoundError):
			pass
		word_features, documents = import_and_process(
			f_name, max_word_features)
		common_functions.pickle_me(pickle_path_doc, documents)
		common_functions.pickle_me(pickle_path_wf, word_features)
	else:
		documents = common_functions.get_pickle(pickle_path_doc)
		word_features = common_functions.get_pickle(pickle_path_wf)
	return word_features, documents

if __name__ == '__main__':
	pt, nt = get_2_lists(r'C:\Users\Tom\Google Drive\Programming\Data Science\Projects\twitter_streaming_sent_analysis\training_data\Sentiment Analysis Dataset.csv')
