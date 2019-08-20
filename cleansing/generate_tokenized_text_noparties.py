import __init__
import config as conf
import nltk
import pandas as pd
import os
import re
import load_dataframe
df=load_dataframe.getTokenizedDataFrame()

parties = pd.read_csv(os.path.join(conf.data_dir, "partidos.csv"), index_col=0, header=None)
candidateNames=df["posted_by"].unique()

stopwords=nltk.corpus.stopwords.words("spanish")
stopwords.append("rt")
whitelist = ["no"]

regex = re.compile(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]')
def remove_parties(row):
	row["tokenized_text_noparties"] = [regex.sub('',w.lower()) for w in row["tokenized_text"] if
									   (w.lower() not in ([i.lower() for i in parties.index.values]+[candidate.lower() for candidate in candidateNames]) and ((w.lower() in whitelist) or (w.lower() not in stopwords)) and regex.sub('',w.lower())!='')]
	return row
df = df.apply(remove_parties, axis=1)

df.to_pickle(os.path.join(conf.pickles_dir, "tokenized.pickle"))