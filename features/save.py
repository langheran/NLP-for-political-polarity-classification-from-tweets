import __init__
import load_dataframe as data
import config as conf
import os
import pandas as pd

def save_all(df, prefix):
	df = df[['id', 'proactivo', 'reactivo', 'agresivo', 'provoto'] + [col for col in df.columns if "_"+prefix in col]]
	df.to_pickle(os.path.join(conf.pickles_dir, "{}.pickle".format(prefix)))
	save_excel(df, prefix)

def save_excel(df, prefix):
	writer = pd.ExcelWriter(os.path.join(conf.output_dir, "{}.xlsx".format(prefix)))
	df.to_excel(writer, 'Sheet1')
	writer.close()
	writer.save()

if(__name__=="__main__"):
	df = data.getPickle("w2v")
	save_excel(df, "w2v")