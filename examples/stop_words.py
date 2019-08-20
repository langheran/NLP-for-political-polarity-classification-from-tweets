from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

example_sentence = "Hola cómo estás? que bien que quieres el caballo."
stop_words = set(stopwords.words("spanish"))

words= word_tokenize(example_sentence)

filtered_sentence = []

for w in words:
	if w not in stop_words:
		filtered_sentence.append(w)

print(filtered_sentence)
