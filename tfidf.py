# coding:utf-8
__author__ = 'Casey'

import jieba
import  jieba.posseg as pseg
import os
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import numpy as np

f = open('./Step4textTopK.txt', 'r')
corpus = []
for line in f.readlines():
	corpus.append(line)

f = open('./data/target.txt', 'r')
target = []
for line in f.readlines():
	target.append(line)

X_train, X_test, y_train, y_test = train_test_split(corpus,	target, test_size = 0.4, random_state = 30)

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer

clf_1 = Pipeline([
    ('vect', CountVectorizer()),
    ('clf', MultinomialNB()),
])
clf_2 = Pipeline([
    ('vect', HashingVectorizer(non_negative=True)),
    ('clf', MultinomialNB()),
])
clf_3 = Pipeline([
    ('vect', TfidfVectorizer()),
    ('clf', MultinomialNB(alpha=0.01)),
])



from sklearn.cross_validation import cross_val_score, KFold
from scipy.stats import sem

def evaluate_cross_validation(clf, X, y, K):
	cv = KFold(len(y), K, shuffle=True, random_state=0)
	scores = cross_val_score(clf, X, y, cv=cv)
	print scores
	print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))


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

# evaluate_cross_validation(clf_3, corpus, target, 5)
train_and_evaluate(clf_3, X_train, X_test, y_train, y_test)
clf_3.named_steps['vect'].get_feature_names()

'''
if __name__ == "__main__":
	vectorizer = CountVectorizer()# 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
	transformer = TfidfTransformer()#该类会统计每个词语的tf-idf权值
	tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
	word = vectorizer.get_feature_names()#获取词袋模型中的所有词语
	weight = tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
	for i in range(1):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
		print "-----第",i,"类文本的赐予tf-idf权重-----"
		for j in range(len(word)):
			print word[j],weight[i][j]
'''