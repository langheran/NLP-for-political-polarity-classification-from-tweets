import __init__
import config as conf
import os
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.naive_bayes import BernoulliNB
import load_dataframe as dt
from features import (
	ExtractFeatures as feat,
	ExtractBOW as bow,
	ExtractW2V as w2v,
	ExtractBIG as big
)
import load_dataframe as data
from testing import test_classifier as tc
from testing import plot_auc_cv as auc
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

def AUC(classifier, *args):
	if(type(args[0]).__name__=="DataFrame"):
		df = args[0]
		feature_names = args[1]
	else:
		df = dt.getTokenizedDataFrame()
		df, feature_names = feat.ExtractFeatures(df, *args)
		df = df.rename_axis(None)
	attitudes=["proactivo", "reactivo", "agresivo", "provoto"]
	f, axarr = plt.subplots(1, 4, figsize=(18,4), sharey=True)
	for i, attitude in enumerate(attitudes):
		sorted_train_labels = sorted(list(set(df.loc[:, attitude])))
		for label in sorted_train_labels:
			t = df[(df[attitude]==label)]
			if t.shape[0]<10:
				df = df.append([t]*10)
		print("========================={}===========================".format(attitude.upper()))
		data=df.loc[:, [c  for c in df.columns for feature_name in feature_names if "_"+feature_name.lower() in c]]
		target=df.loc[:, attitude]

		train_data, test_data, train_labels, test_labels = train_test_split(data, target, train_size=0.6, stratify=target, random_state=conf.seed)
		precision, recall, accuracy, f1, classifier_name, learning_time, prediction_time = tc.test_classifier(train_data, train_labels, test_data, test_labels, classifier)
		auc.plot_auc_cv(data, target, classifier, "Attitude '{}'".format(attitude), save=conf.images_dir, plot=axarr[i])
	plt.setp([a.get_yticklabels() for a in axarr[1:]], visible=False)
	f.subplots_adjust(hspace=0.3)
	plt.suptitle('{}+{} for all attributes'.format("+".join([feature_name.upper() for feature_name in feature_names]),classifier_name), y=1)
	f.text(0.5, 0.01, 'False Positive Rate', ha='center')
	f.text(0.09, 0.5, 'True Positive Rate', va='center', rotation='vertical')
	plt.savefig(os.path.join(conf.images_dir, '{}+{} for all attributes.png'.format(
		"+".join([feature_name.upper() for feature_name in feature_names]), classifier_name)), bbox_inches='tight')
	# plt.show()


if(__name__=="__main__"):
	classifiers=[
		BernoulliNB()
		# ,RandomForestClassifier(n_estimators=300,n_jobs=-1, random_state=conf.seed)
	]
	tests=[["bow"],["big"],["w2v"],["bow","big"],["bow","w2v"],["big","w2v"],["big","w2v","bow"]]
	for classifier in classifiers:
		for test in tests:
			AUC(classifier, data.getFeaturesDataFrame(*test), test)
			# AUC(BernoulliNB(), bow.ExtractW2V)
			# AUC(BernoulliNB(), bow.ExtractBOW, w2v.ExtractW2V, big.ExtractBIG)