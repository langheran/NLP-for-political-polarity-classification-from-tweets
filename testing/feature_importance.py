from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
import __init__
import matplotlib.pyplot as plt
import numpy as np
import load_dataframe as dat
import config as conf
feature_names=["big", "w2v", "bow"]
df=dat.getFeaturesDataFrame(*feature_names)
classifier=RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=conf.seed)
attitudes = ["proactivo", "reactivo", "agresivo", "provoto"]
for i, attitude in enumerate(attitudes):
	data = df.loc[:, [c for c in df.columns for feature_name in feature_names if "_" + feature_name.lower() in c]]
	target = df.loc[:, attitude]
	train_data, test_data, train_labels, test_labels= train_test_split(data, target, test_size=.5,random_state=0)
	model = classifier.fit(train_data, train_labels)
	importances = model.feature_importances_
	std = np.std([tree.feature_importances_ for tree in model.estimators_],
				 axis=0)
	indices = np.argsort(importances)[::-1]
	max_features=25
	plt.figure()
	title='{}+RandomForest feature importance for attitude {}'.format(
		"+".join([feature_name.upper() for feature_name in feature_names]), attitude)
	plt.title(title)
	plt.bar(range(train_data.shape[1])[:max_features], importances[indices[:max_features]],
			color="r", yerr=std[indices[:max_features]], align="center")
	plt.xticks(range(train_data.shape[1])[:max_features], df.columns[indices[:max_features]])
	locs, labels = plt.xticks()
	plt.setp(labels, rotation=90)
	plt.xlim([-1, max_features])
	fig = plt.gcf()
	fig.set_size_inches(18.5, 10.5)
	plt.savefig(os.path.join(conf.images_dir, title+'.png'),
				bbox_inches='tight')