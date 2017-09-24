import os
import nltk
from nltk.tokenize import word_tokenize
import random
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
import common_functions
# import data_importer_short_reviews as data_importer
import data_importer_sentiment_analysis_dataset as data_importer


# Gets rid of some warnings in output text
import warnings
warnings.filterwarnings("ignore")

file_name = 'sentiment_analysis_dataset.csv'

light_mode = False  # True when only using pre-trained classifiers,
# and don't need to re-evaluate accuracy
percent_train = 90
classifiers_to_use = [
	'NaiveBayesClassifier',
	'MultinomialNB',
	'BernoulliNB',
	'LogisticRegression',
	'LinearSVC',
	'SGDClassifier']


def tt_split(input_data, percent_tr):
	# train, test split
	change_index = (
		len(input_data) -
		int(len(input_data) * (1 - (percent_tr / 100.0))))
	tr_set = input_data[:change_index]
	te_set = input_data[change_index:]
	return tr_set, te_set


def try_train_classifier(f_name, c_name, tr_set, te_set):
	currentPath = str(os.path.dirname(os.path.realpath(__file__)))
	rel_folder_path = r'\Pickles\\'
	pickle_path_c = (
		currentPath + rel_folder_path + f_name[:-4] + '_' + c_name + '.pickle')
	if not os.path.isfile(pickle_path_c):
		if c_name == 'NaiveBayesClassifier':
			classifier = nltk.NaiveBayesClassifier.train(tr_set)
		else:
			classifier = eval('SklearnClassifier(' + c_name + '())')
			classifier.train(tr_set)
		common_functions.pickle_me(pickle_path_c, classifier)
		accuracy = round(float(nltk.classify.accuracy(classifier, te_set)) * 100, 1)
	else:
		classifier = common_functions.get_pickle(pickle_path_c)
		accuracy = None
	# accuracy = round(float(nltk.classify.accuracy(classifier, te_set)) * 100, 1)
	return classifier, accuracy


def try_train_all_classifiers(f_name, input_c_names, tr_set, te_set):
	c_list = []
	currentPath = str(os.path.dirname(os.path.realpath(__file__)))
	rel_folder_path = r'\Pickles\\'
	pickle_path_acc = (
		currentPath + rel_folder_path + f_name[:-4] + '_acc_dict.pickle')
	if not os.path.isfile(pickle_path_acc):
		acc_dict = {}
	else:
		acc_dict = common_functions.get_pickle(pickle_path_acc)
		os.remove(pickle_path_acc)
	for i in range(len(input_c_names)):
		c, acc = try_train_classifier(f_name, input_c_names[i], tr_set, te_set)
		c_list.append(c)
		if acc is not None:
			acc_dict[input_c_names[i]] = acc
	acc_dict_mod = acc_dict

	common_functions.pickle_me(pickle_path_acc, acc_dict_mod)
	return c_list, acc_dict_mod


class VoteClassifier(ClassifierI):
	def __init__(self, *classifiers):
		self._classifiers = classifiers

	def classify(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)

		return mode(votes)

	def classify_w(self, features, acc_weights):
		# version of classify with votes weighted by accuracy of algo
		votes = []
		for index, classifier in enumerate(self._classifiers):
			v = classifier.classify(features)
			if v == 'pos':
				votes.append(acc_weights[index])
			elif v == 'neg':
				votes.append(acc_weights[index] * -1)
			else:
				print("error in v")
		pos_score, neg_score = 0, 0
		for vote in votes:
			if vote >= 0:
				pos_score += vote
			elif vote < 0:
				neg_score += -1 * vote
		if pos_score > neg_score:
			return 'pos'
		elif neg_score > pos_score:
			return 'neg'
		else:
			print("ERROR: neg, pos scores are equal")
			if random.randint(0, 1) == 0:
				return 'pos'
			else:
				return 'neg'

	def confidence(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		if votes.count('pos') == votes.count('neg'):
			return 0.5
		else:
			choice_votes = votes.count(mode(votes))
			conf = choice_votes / len(votes)
		return conf


def generate_class_inp_str(c_list):
	result_string = ''
	for i, j in enumerate(c_list):
		result_string += 'classifiers[' + str(i) + ']'
		if i != len(c_list) - 1:
			result_string += ', '
	return result_string


word_features, documents = data_importer.process(
	file_name, min_score_for_pos, max_word_features=5000)

if light_mode:
	training_set, testing_set = [], []
else:
	featuresets = common_functions.doc_process(
		file_name, documents, word_features)
	random.shuffle(featuresets)

	training_set, testing_set = tt_split(featuresets, percent_train)

classifiers, classifier_accuracies = try_train_all_classifiers(
	file_name, classifiers_to_use, training_set, testing_set)

print('\n', classifier_accuracies)
acc_values = [classifier_accuracies[key] for key in classifier_accuracies.keys() if key in classifiers_to_use]
print(acc_values)

voted_classifier = eval(
	'VoteClassifier(' + generate_class_inp_str(classifiers) + ')')


def sentiment(text):
	feats = common_functions.find_features(text, word_features)
	# return voted_classifier.classify(feats), voted_classifier.confidence(feats)
	return voted_classifier.classify_w(feats, acc_values), voted_classifier.confidence(feats)

if __name__ == '__main__':
	from time import time as tt
	t_1 = tt()
	print(sentiment("good item, handy tool, breaks easily however, awful"))
	print(tt() - t_1, ' s')
