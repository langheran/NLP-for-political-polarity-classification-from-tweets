import itertools

from features import SpecialTokens as st
from features import save
import numpy as np
import pandas as pd

def ExtractBIG(df):
	def ngrams(input, n):
		output = []
		for i in range(len(input) - n + 1):
			output.append(input[i:i + n])
		return output

	concat_df = df.copy(deep=True)
	def get_special_token(w):
		for token in st.special_tokens:
			if(token(w)):
				return token.__name__.replace('is_','')
		return None
	def split_row(row):
		row["special_tokens"]=[get_special_token(w) for w in row["text"].split(" ") if get_special_token(w) is not None]
		return row
	token_names=[t.__name__.replace('is_','') for t in st.special_tokens]
	concat_df = concat_df.apply(split_row, axis=1)

	columns = ['id'] + list(map(lambda c: str(c) + "-count_big", token_names))
	rows=[]
	for idx in concat_df.index.values:
		row = np.zeros(len(columns)-1)
		tokens=concat_df.loc[idx]["special_tokens"]
		for token in tokens:
			index=token_names.index(token)
			row[index]=row[index]+1
		rows.append([]+[concat_df.loc[idx]["id"]] + list(row))
	new_df = pd.DataFrame(rows, columns=columns)
	new_df.set_index("id", inplace=True, drop=False)
	concat_df = pd.merge(concat_df, new_df, on='id', how='inner')
	concat_df.set_index("id", inplace=True, drop=False)

	all_bigrams=[list(p) for p in itertools.product(token_names,repeat=2)]
	columns = ['id'] + list(map(lambda c: str(c) + "-bigram_big", ["-".join(p) for p in all_bigrams]))
	rows = []
	for idx in concat_df.index.values:
		bigrams = ngrams(concat_df.loc[idx]["special_tokens"],2)
		rows.append([concat_df.loc[idx]["id"]] + [sum(1 for bg in bigrams if bg==b) for b in all_bigrams])
	new_df = pd.DataFrame(rows, columns=columns)
	new_df.set_index("id", inplace=True, drop=False)
	result = pd.merge(concat_df, new_df, on='id', how='inner')
	result = result.loc[:, ~result.columns.duplicated()]
	return result

if(__name__=="__main__"):
	import load_dataframe
	df = load_dataframe.getTokenizedDataFrame()
	concat_df=ExtractBIG(df)
	save.save_all(concat_df, "big")
