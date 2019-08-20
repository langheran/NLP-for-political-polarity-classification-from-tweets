import __init__
import itertools
import pandas as pd
import nltk
import plotly
import plotly.graph_objs as go
import load_dataframe as data

def printHistogram(df, name, column_name="tokenized_text"):
	def get_words(df):
		words=[]
		for s in df[column_name].values:
			for w in s:
				words.append(w.lower())
		stopwords=nltk.corpus.stopwords.words("spanish")
		stopwords.append("rt")
		whitelist = ["no"]
		words=[word for word in words if (word in whitelist) or (word not in stopwords)]
		return words
	all_words=get_words(df)
	all_words = nltk.FreqDist(all_words)
	# print(all_words.most_common(100))
	# word_features = list(all_words.keys())[:10]
	# print(word_features)
	word_df = pd.DataFrame(data={"word": [k for k, v in all_words.most_common(15)],
										 "occurrences": [v for k, v in all_words.most_common(15)]},
								   columns=["word", "occurrences"])

	x_words = list(word_df.loc[0:15,"word"])

	attitudes=["provoto", "agresivo", "reactivo", "proactivo"]
	dist = []
	for attitude in attitudes:
		attitude_words=get_words(df[(df[attitude] > 0.0)])
		attitude_words = nltk.FreqDist(attitude_words)
		dist.append(go.Bar(
				x = x_words,
				y = [attitude_words[w]for w in x_words],
				name = attitude
		))

	fig = go.Figure(data=dist, layout=go.Layout(title="Top words by category"))
	plotly.offline.plot(fig, filename='images/wordlist-category-histogram-'+name+'.html')

df=data.getTokenizedDataFrame()
printHistogram(df, "with-proactivo", "tokenized_text_noparties")
df=df[(df["provoto"] > 0.0) | (df["agresivo"] > 0.0) | (df["reactivo"] > 0.0)]
printHistogram(df, "regardless-of-proactivo", "tokenized_text_noparties")