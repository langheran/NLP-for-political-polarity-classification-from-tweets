# Code taken from sklearn official website @ http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html#sphx-glr-auto-examples-model-selection-plot-roc-crossval-py

import numpy as np
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split

# #############################################################################
# Classification and ROC analysis
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
import os


def plot_auc_cv(X, y, classifier, title='Some extension of Receiver operating characteristic to multi-class', save=None, plot=None):
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

	# Compute micro-average ROC curve and ROC area
	fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
	roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
	lw = 2

	##############################################################################
	# Plot ROC curves for the multiclass problem

	# Compute macro-average ROC curve and ROC area

	# First aggregate all false positive rates
	all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

	# Then interpolate all ROC curves at this points
	mean_tpr = np.zeros_like(all_fpr)
	for i in range(n_classes):
		mean_tpr += interp(all_fpr, fpr[i], tpr[i])

	# Finally average it and compute AUC
	mean_tpr /= n_classes

	fpr["macro"] = all_fpr
	tpr["macro"] = mean_tpr
	roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

	grid=False
	if(plot is None):
		plot=plt
		plot.figure()
	else:
		grid=True

	# Plot all ROC curves

	# plt.plot(fpr["micro"], tpr["micro"],
	# 		 label='micro-average ROC curve (area = {0:0.2f})'
	# 			   ''.format(roc_auc["micro"]),
	# 		 color='deeppink', linestyle=':', linewidth=4)

	if(grid):
		plot.plot(fpr["macro"], tpr["macro"],
				  label='macro-average ROC curve',
				  color='navy', linestyle=':', linewidth=4)
	else:
		plot.plot(fpr["macro"], tpr["macro"],
			 label='macro-average ROC curve (area = {0:0.2f})'
				   ''.format(roc_auc["macro"]),
			 color='navy', linestyle=':', linewidth=4)

	# colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
	# for i, color in zip(range(n_classes), colors):
	# 	plt.plot(fpr[i], tpr[i], color=color, lw=lw,
	# 			 label='ROC curve of class {0} (area = {1:0.2f})'
	# 				   ''.format(i, roc_auc[i]))

	plot.plot([0, 1], [0, 1], 'k--', lw=lw)
	if (not grid):
		plot.xlim([0.0, 1.0])
		plot.ylim([0.0, 1.05])
		plot.xlabel('False Positive Rate')
		plot.ylabel('True Positive Rate')
		plot.title(title)
		plot.legend(loc="lower right")
	else:
		plot.set_xlim([0.0, 1.0])
		plot.set_ylim([0.0, 1.05])
		# plot.set_xlabel('False Positive Rate')
		# plot.set_ylabel('True Positive Rate')
		plt.legend(loc="lower right")
		title_auc='{0} (area = {1:0.2f})'.format(title, roc_auc["macro"])
		plot.set_title(title_auc)
	if(save is not None):
		if (not grid):
			plot.savefig(os.path.join(save,'{}.png'.format(title)), bbox_inches='tight')
	else:
		if(not grid):
			plot.show()

if(__name__=="__main__"):
	iris = datasets.load_iris()
	X = iris.data
	y = iris.target
	X, y = X[y != 2], y[y != 2]
	classifier = svm.SVC(kernel='linear', probability=True,
						 random_state=np.random.RandomState(0))
	plot_auc_cv(X, y, classifier)
