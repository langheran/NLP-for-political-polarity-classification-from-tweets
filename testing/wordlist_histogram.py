import __init__
import pandas as pd
import nltk
import plotly
import plotly.graph_objs as go
import load_dataframe as data
df=data.getTokenizedDataFrame()

df = df[(df["proactivo"] > 0.0) | (df["provoto"] > 0.0) | (df["agresivo"] > 0.0) | (df["reactivo"] > 0.0)]
all_words=[]
for s in df["tokenized_text"].values:
	for w in s:
		all_words.append(w.lower())
stopwords=nltk.corpus.stopwords.words("spanish")
stopwords.append("rt")
whitelist = ["no"]
all_words=[word for word in all_words if (word in whitelist) or (word not in stopwords)]
all_words = nltk.FreqDist(all_words)
# print(all_words.most_common(100))
# word_features = list(all_words.keys())[:10]
# print(word_features)
word_df = pd.DataFrame(data={"word": [k for k, v in all_words.most_common(100)],
                                     "occurrences": [v for k, v in all_words.most_common(100)]},
                               columns=["word", "occurrences"])

x_words = list(word_df.loc[0:15,"word"])
x_words.reverse()
y_occ = list(word_df.loc[0:15,"occurrences"])
y_occ.reverse()

dist = [
    go.Bar(
        x=y_occ,
        y=x_words,
        orientation="h"
)]
fig = go.Figure(data=dist, layout=go.Layout(title="Top words in built wordlist"))
plotly.offline.plot(fig, filename='images/word-list.html')