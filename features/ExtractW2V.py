import sys

import __init__
import config as conf
import os
import itertools
from time import time
import pandas as pd
import nltk
import numpy as np
from features.w2v import w2v
from features import save
import config as conf

def ExtractW2V(df):
	model = w2v()
	now = time()
	model.load(conf.w2v_model_bin)
	loading_time = time()-now
	columns=['id']+list(map(lambda i: str(i) + "_w2v", range(model.dimensions)))
	concat_df = df.copy(deep=True)
	rows=[]
	for idx in concat_df.index.values:
		tokens=concat_df.loc[idx]["tokenized_text_noparties"]
		w2v_vectors=[]
		for _, w in enumerate(tokens):
			vec = model.get_vector(w.lower())
			if(vec is not None and type(vec).__name__=="ndarray"):
				w2v_vectors.append(vec)
				w2v_vectors.append(vec)
		if(len(w2v_vectors)>0):
			w2v_vector_avg = list(np.array(w2v_vectors).mean(axis=0))
			rows.append([concat_df.loc[idx]["id"]]+w2v_vector_avg)
	new_df =  pd.DataFrame(rows, columns=columns)
	new_df.set_index("id", inplace=True, drop=False)
	result = pd.merge(concat_df,new_df, on='id', how='inner')
	result = result.loc[:, ~result.columns.duplicated()]
	return result

if(__name__=="__main__"):
	import load_dataframe
	df = load_dataframe.getTokenizedDataFrame()
	concat_df=ExtractW2V(df)
	save.save_all(concat_df, "w2v")
	with pd.option_context('display.max_rows', None, 'display.max_columns', 10, 'display.max_colwidth', -1, 'display.float_format', lambda x: '%.3f' % x):
		print(concat_df.head(5))