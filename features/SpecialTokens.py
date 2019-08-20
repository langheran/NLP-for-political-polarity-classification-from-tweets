import re
from features.w2v import w2v
import config as conf
import pandas as pd

exclamation_regex = re.compile(r'^[\w]*\!$')
question_regex = re.compile(r'^[\w]*\?$')
ellipsis_regex = re.compile(r'^[\w]*\.\.\.$')
mention_regex = re.compile(r'^(?!.*\bRT\b)(?:.+\s)?@\w+$')
alphanumeric_regex = re.compile(u'^[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ:\_\-]$')
hashtag_regex = re.compile(r'^#(\w+)$')
quote_regex = re.compile(r"""^(([\"\'](.+?)[\"\'])|([\"\'](.+?))|((.+?)[\"\']))$""")
url_regex = re.compile(r"^http.?://[^\s]+[\s]?$")
colon_regex = re.compile(r'^(([\w]*)[\:])$')
semicolon_regex = re.compile(r'^(([\w]*)[\;])$')
comma_regex = re.compile(r'^(([\w]*)[\,])$')

model = w2v()
model.load(conf.w2v_model_bin)
pos_emoticons = pd.read_csv(conf.pos_emoticons_csv, index_col=0, header=None, sep='%')
neg_emoticons = pd.read_csv(conf.neg_emoticons_csv, index_col=0, header=None , sep='%')

def is_uppercase(w):
	return w == w.upper()


def is_exclamation(w):
	return bool(re.search(exclamation_regex, w))


def is_question(w):
	return bool(re.search(question_regex, w))


def is_ellipsis(w):
	return bool(re.search(ellipsis_regex, w))


def is_alphanumeric(w):
	return bool(re.search(alphanumeric_regex, w))


def is_name(w):
	return is_alphanumeric(w) and w not in model.model.vocab


def is_mention(w):
	return bool(re.search(mention_regex, w))


def is_hashtag(w):
	return bool(re.search(hashtag_regex, w))


def is_quoted(w):
	return bool(re.search(quote_regex, w))


def is_url(w):
	return bool(re.search(url_regex, w))


def is_pos_emoticon(w):
	return w in pos_emoticons.index.values


def is_neg_emoticon(w):
	return w in neg_emoticons.index.values


def is_colon(w):
	return bool(re.search(colon_regex, w))


def is_semicolon(w):
	return bool(re.search(semicolon_regex, w))


def is_comma(w):
	return bool(re.search(comma_regex, w))


special_tokens = [
	is_ellipsis,
	is_exclamation,
	is_hashtag,
	is_mention,
	is_name,
	is_neg_emoticon,
	is_pos_emoticon,
	is_question,
	is_quoted,
	is_uppercase,
	is_url,
	is_colon,
	is_semicolon,
	is_comma
]