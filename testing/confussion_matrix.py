import matplotlib.pyplot as plt
import plotly
from plotly import graph_objs as go
from sklearn import metrics
from sklearn.model_selection import train_test_split
import os

import load_dataframe as dat
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from features import (
	ExtractFeatures as feat,
	ExtractBOW as bow,
	ExtractW2V as w2v,
	ExtractBIG as big
)
import config as conf
import numpy as np
from testing import test_classifier as tc

def confusion_matrix(classifier, df, feature_names):
	classifier_name=type(classifier).__name__
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

		roc_auc = tc.compute_auc_multiclass(data, target, classifier)
		train_data, test_data, train_labels, test_labels = train_test_split(data, target, train_size=0.6, stratify=target,
																		random_state=conf.seed)

		model = classifier.fit(train_data, train_labels)
		predicted_labels = model.predict(test_data)
		conf_arr=metrics.confusion_matrix(test_labels,predicted_labels)
		norm_conf = []
		for x in conf_arr:
			a = 0
			tmp_arr = []
			a = sum(x, 0)
			for j in x:
				tmp_arr.append(float(j)/float(a))
			norm_conf.append(tmp_arr)

		plot = plt
		fig = plot.figure()
		plot.clf()
		ax = fig.add_subplot(111)
		ax.set_aspect(1)
		res = ax.imshow(np.array(norm_conf), cmap=plot.cm.jet,
						interpolation='nearest')

		width, height = conf_arr.shape

		for x in range(width):
			for y in range(height):
				ax.annotate(str(conf_arr[x][y]), xy=(y, x),
							horizontalalignment='center',
							verticalalignment='center')

		cb = fig.colorbar(res)
		alphabet = sorted_train_labels
		title="Attitude '{}'".format(attitude)
		title='{0} (ROC area = {1:0.2f})'.format(title, roc_auc)
		plot.title(title)
		plot.xticks(range(width), alphabet[:width])
		plot.yticks(range(height), alphabet[:height])
		experiment_dir=os.path.join(conf.images_dir,'confusion-matrix', '{}+{}'.format("+".join([feature_name.upper() for feature_name in feature_names]), classifier_name))
		if not os.path.exists(experiment_dir):
			os.makedirs(experiment_dir)
		plt.savefig(os.path.join(experiment_dir, '{}+{} for attitude {} confusion matrix.png'.format("+".join([feature_name.upper() for feature_name in feature_names]), classifier_name,attitude)), bbox_inches='tight')

def plot_auc_barchart(classifiers, tests):
	attitudes = ["proactivo", "reactivo", "agresivo", "provoto"]
	results={}
	dfs = {}
	for classifier in classifiers:
		classifier_name = type(classifier).__name__
		for feature_names in tests:
			feature = "+".join([feature_name.upper() for feature_name in feature_names] + [classifier_name])
			dfs[feature]=dat.getFeaturesDataFrame(*feature_names)
	for i, attitude in enumerate(attitudes):
		results[attitude]={}
		for classifier in classifiers:
			classifier_name = type(classifier).__name__
			for feature_names in tests:
				feature = "+".join([feature_name.upper() for feature_name in feature_names] + [classifier_name])
				df = dfs[feature]
				sorted_train_labels = sorted(list(set(df.loc[:, attitude])))
				for label in sorted_train_labels:
					t = df[(df[attitude] == label)]
					if t.shape[0] < 10:
						df = df.append([t] * 10)
				print("========================={}===========================".format(attitude.upper()))
				data = df.loc[:, [c for c in df.columns for feature_name in feature_names if "_" + feature_name.lower() in c]]
				target = df.loc[:, attitude]
				results[attitude][feature]= tc.compute_auc_multiclass(data, target, classifier)

		attitudes = ["provoto", "agresivo", "reactivo", "proactivo"]
		dist = []
		for attitude in attitudes:
			dist.append(go.Bar(
				x=list(results[attitude].keys()),
				y=[results[attitude][r] for r in results[attitude].keys()],
				name=attitude
			))

		fig = go.Figure(data=dist, layout=go.Layout(title="Average ROC AUC per attitude"))
		plotly.offline.plot(fig, filename='images/{}-average-roc-auc-per-attitude.html'.format(classifier_name))

def plot_confusion_matrix(classifiers, tests):
	for classifier in classifiers:
		for test in tests:
			confusion_matrix(classifier, dat.getFeaturesDataFrame(*test), test)

if(__name__=="__main__"):
	classifiers = [
		BernoulliNB(),
		RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=conf.seed)
	]
	tests = [["bow"], ["big"], ["w2v"], ["bow", "big"], ["bow", "w2v"], ["big", "w2v"], ["big", "w2v", "bow"]]
	# plot_confusion_matrix(classifiers, tests)
	plot_auc_barchart(classifiers, tests)