from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize

import __init__
import random
from time import time
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score, roc_auc_score, roc_curve, auc
from sklearn.model_selection import cross_val_score, train_test_split
import numpy as np
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
import config as conf
import load_dataframe as dat

def test_classifier(train_data, train_labels, test_data, test_labels, classifier, printResults=True):
	classifier_name = str(type(classifier).__name__)
	now = time()
	sorted_train_labels = sorted(list(set(train_labels)))
	model = classifier.fit(train_data, train_labels)
	learning_time = time() - now
	now = time()
	predicted_labels = model.predict(test_data)
	prediction_time = time() - now
	precision = precision_score(test_labels, predicted_labels, average=None, pos_label=None, labels=sorted_train_labels)
	recall = recall_score(test_labels, predicted_labels, average=None, pos_label=None, labels=sorted_train_labels)
	accuracy = accuracy_score(test_labels, predicted_labels)
	f1 = f1_score(test_labels, predicted_labels, average=None, pos_label=None, labels=sorted_train_labels)
	if(printResults):
		print("========================{}==========================".format(classifier_name))
		print("                  " + '\t'.join(['{:1.0f}     '.format(i) for i in sorted_train_labels]))
		print("Precision         " + '\t'.join(['{:2.4f}'.format(i) for i in precision]))
		print("Recall            " + '\t'.join(['{:2.4f}'.format(i) for i in recall]))
		print("Accuracy          " + str(accuracy))
		print("F1                " + '\t'.join(['{:2.4f}'.format(i) for i in f1]))
		print("========================{}==========================".format(classifier_name))
	return precision, recall, accuracy, f1, classifier_name, learning_time, prediction_time

def cross_validation(classifier, train_data, train_labels, printResults=True):
	classifier_name = str(type(classifier).__name__)
	now = time()
	accuracy = [cross_val_score(classifier, train_data, train_labels, cv = 8, n_jobs=-1)]
	crossvalidation_time = time() - now
	accuracy_avg=np.array(accuracy[0]).mean()
	if(printResults):
		print("========================{}==========================".format(classifier_name))
		print("                  " + '\t'.join(range(1,8)))
		print("Accuracy          " + str(accuracy[0]))
		print("Accuracy average  " + str(accuracy_avg))
		print("========================{}==========================".format(classifier_name))
	return accuracy, accuracy_avg, classifier_name, crossvalidation_time

def get_accuracy(classifier, df, feature_names):
	classifier_name = type(classifier).__name__
	attitudes = ["proactivo", "reactivo", "agresivo", "provoto"]
	for i, attitude in enumerate(attitudes):
		sorted_train_labels = sorted(list(set(df.loc[:, attitude])))
		for label in sorted_train_labels:
			t = df[(df[attitude] == label)]
			if t.shape[0] < 10:
				df = df.append([t] * 10)
		print("========================={}===========================".format(attitude.upper()))
		data = df.loc[:, [c for c in df.columns for feature_name in feature_names if "_" + feature_name.lower() in c]]
		target = df.loc[:, attitude]
		train_data, test_data, train_labels, test_labels = train_test_split(data, target, train_size=0.6,stratify=target, random_state=conf.seed)
		precision, recall, roc_auc, accuracy, f1, classifier_name, learning_time, prediction_time = test_classifier(train_data, train_labels, test_data, test_labels, classifier)

def compute_auc_multiclass(X, y, classifier):
	# Code taken from sklearn official website
	# Binarize the output
	y = label_binarize(y, classes=list(set(y)))
	n_classes = y.shape[1]

	# Add noisy features to make the problem harder
	n_samples, n_features = X.shape

	# shuffle and split training and test sets
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5,
														random_state=0)

	# Learn to predict each class against the other
	classifier = OneVsRestClassifier(classifier)
	y_score = classifier.fit(X_train, y_train).predict_proba(X_test)

	# Compute ROC curve and ROC area for each class
	fpr = dict()
	tpr = dict()
	roc_auc = dict()
	for i in range(n_classes):
		fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
		roc_auc[i] = auc(fpr[i], tpr[i])

		# Plot ROC curves for the multiclass problem

		# Compute macro-average ROC curve and ROC area

		# First aggregate all false positive rates
	all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

	# Then interpolate all ROC curves at this points
	mean_tpr = np.zeros_like(all_fpr)
	for i in range(n_classes):
		mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

	# Finally average it and compute AUC
	mean_tpr /= n_classes

	fpr["macro"] = all_fpr
	tpr["macro"] = mean_tpr
	roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
	return roc_auc["macro"]

if(__name__=="__main__"):
	classifiers=[
		BernoulliNB(),
		RandomForestClassifier(n_estimators=300,n_jobs=-1, random_state=conf.seed)
	]
	tests=[["bow"],["big"],["w2v"],["bow","big"],["bow","w2v"],["big","w2v"],["big","w2v","bow"]]
	for classifier in classifiers:
		for test in tests:
			get_accuracy(classifier, dat.getFeaturesDataFrame(*test), test)