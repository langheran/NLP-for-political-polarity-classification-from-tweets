import __init__
import config as conf
import os
import itertools
import pandas as pd
import nltk
import numpy as np
from features import save

def ExtractBOW(df):
	words=itertools.chain.from_iterable(df["tokenized_text_noparties"])
	words=nltk.FreqDist(words).most_common(1000)
	words=[k for k, v in words]
	columns=['id']+list(map(lambda w: w + "_bow", words))
	concat_df = df.copy(deep=True)

	rows=[]
	for idx in concat_df.index.values:
		tokens=concat_df.loc[idx]["tokenized_text_noparties"]
		rows.append([concat_df.loc[idx]["id"]]+[1 if w in tokens else 0 for _, w in enumerate(words)])
	new_df =  pd.DataFrame(rows, columns=columns)
	new_df.set_index("id", inplace=True, drop=False)
	result = pd.concat([concat_df,new_df], axis=1)
	result = result.loc[:, ~result.columns.duplicated()]
	return result

if(__name__=="__main__"):
	import load_dataframe
	df = load_dataframe.getTokenizedDataFrame()
	concat_df=ExtractBOW(df)
	save.save_all(concat_df, "bow")
	with pd.option_context('display.max_rows', None, 'display.max_columns', 10, 'display.max_colwidth', -1, 'display.float_format', lambda x: '%.3f' % x):
		print(concat_df[(concat_df['no_bow']>0)][['filename','text','tokenized_text_noparties','no_bow']].head(5))
	print(concat_df.head(5))