import __init__
import config as conf
import os
import nltk
from nltk.stem import SnowballStemmer
import pandas as pd
import re

class CustomTokenizer():
	def __init__(self, data):
		self.data = data
	def stem(self, stemmer = SnowballStemmer('spanish')):
		def stem_and_join(row):
			row["stemmed_text"] = list(map(lambda str: stemmer.stem(str.lower()), row["text"]))
			return row
		self.data=self.data.apply(stem_and_join, axis=1)

	def tokenize(self, tokenizer=nltk.word_tokenize):
		def tokenize_row(row):
			row["tokenized_text"]=[]+tokenizer(row["clean_text"])
			return row
		self.cleanup()
		self.data = self.data.apply(tokenize_row, axis=1)

	def cleanup(self):
		def regex_replace(expression):
			self.data["clean_text"].replace(expression, "", inplace=True)
		def delete_uris():
			regex_replace(re.compile(r"http.?://[^\s]+[\s]?"))
		def delete_special_characters():
			for delete in map(lambda r: re.compile(re.escape(r)), [",", ":", "\"", "=", "&", ";", "%", "$", "@[A-Za-z0-9_\-]*", "%", "^", "*", "(", ")", "{", "}", "[", "]", "|", "/", "\\", ">", "<", "-","!", "?", ".", "'","--", "---", "#[A-Za-z0-9_\-]*"]):
				data["clean_text"].replace(delete, "", inplace=True)
		def delete_mentions():
			regex_replace(re.compile(r"@[^\s]+[\s]?"))
		def delete_digits():
			regex_replace(re.compile(r"\s?[0-9]+\.?[0-9]*"))
		self.data["clean_text"] = self.data["text"]
		delete_uris()
		delete_special_characters()
		delete_mentions()
		delete_digits()

if(__name__=="__main__"):
	data = pd.read_pickle(os.path.join(conf.pickles_dir, "final.pickle"))
	tokenizer = CustomTokenizer(data)
	tokenizer.tokenize()
	tokenizer.stem()
	tokenizer.data.to_pickle(os.path.join(conf.pickles_dir, "tokenized.pickle"))
	print(tokenizer.data.head(5))