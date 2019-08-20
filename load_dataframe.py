import pandas as pd
import os
import config as conf
import numpy as np

def getTokenizedDataFrame():
	df = pd.read_pickle(os.path.join(conf.pickles_dir, "tokenized.pickle"))
	df = df[(df["proactivo"] > 0.0) | (df["provoto"] > 0.0) | (df["agresivo"] > 0.0) | (df["reactivo"] > 0.0)]
	return df

def getPickle(name):
	df = pd.read_pickle(os.path.join(conf.pickles_dir, "{}.pickle".format(name)))
	return df


def getFeaturesDataFrame(*args):
	import numpy as np
	np.set_printoptions(threshold=np.nan)
	df = getPickle(args[0])
	df = df[list(set(df.columns))]
	for feat_id in range(len(args)-1):
		new_df = getPickle(args[feat_id+1])
		new_df = new_df[["id"]+list(set(new_df.columns) - set(df.columns))]
		df = df.loc[:, ~df.columns.duplicated()]
		new_df = new_df.loc[:, ~new_df.columns.duplicated()]
		df=pd.merge(df, new_df, on='id', how='inner')
	return df

if(__name__=="__main__"):
	df=getTokenizedDataFrame()
	writer = pd.ExcelWriter(os.path.join(conf.output_dir, "Final.xlsx"))
	df.to_excel(writer, 'Sheet1')
	writer.close()
	writer.save()