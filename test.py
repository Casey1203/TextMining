__author__ = 'Casey'

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


from sklearn.datasets import fetch_20newsgroups
from sklearn.cross_validation import cross_val_score, KFold
from scipy.stats import sem #Calculates the standard error of the mean (or standard error of measurement) of the values in the input array.

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer

news = fetch_20newsgroups(subset='all')
#news.keys() ['DESCR', 'data', 'target', 'target_names', 'filenames']
#news.data type:list

SPLIT_PERC = 0.75
split_size = int(len(news.data) * SPLIT_PERC)
X_train = news.data[:split_size]
X_test = news.data[split_size:]
y_train = news.target[:split_size]
y_test = news.target[split_size:]

def evaluate_cross_validation(clf, X, y, K):
	# crete k-fold cross validation iterator of k=5 folds
	cv = KFold(len(y), K, shuffle=True, random_state=0)
	scores = cross_val_score(clf, X, y, cv=cv)# accuracy
	print scores
	print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))

from sklearn import metrics
def train_and_evaluate(clf, X_train, X_test, y_train, y_test):
	clf.fit(X_train, y_train)
	print "Accuracy on training set:"
	print clf.score(X_train, y_train)
	print "Accuracy on testing set:"
	print clf.score(X_test, y_test)

	y_pred = clf.predict(X_test)
	print "Classification Report:"
	print metrics.classification_report(y_test, y_pred)
	print "Confusion Matrix:"
	print metrics.confusion_matrix(y_test, y_pred)



if __name__ == "__main__":
	clf_1 = Pipeline([('vect', CountVectorizer()), ('clf', MultinomialNB()), ])
	clf_2 = Pipeline([('vect', HashingVectorizer(non_negative=True)), ('clf', MultinomialNB()), ])
	clf_3 = Pipeline([('vect', TfidfVectorizer()), ('clf', MultinomialNB(alpha=0.01)), ])

	clfs = [clf_1, clf_2, clf_3]
	#evaluate_cross_validation(clf_3, news.data, news.target, 5)
	# for clf in clfs:
	#	evaluate_cross_validation(clf, news.data, news.target, 5)

	#train_and_evaluate(clf_3, X_train, X_test, y_train, y_test)

	#print clf_3.named_steps['vect'].get_feature_names()
	print news.target_names[:10]
	#print news.target[:10]