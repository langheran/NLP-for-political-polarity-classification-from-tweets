import __init__
import gensim


class w2v(object):
	model = None
	dimensions = 0

	def load(self, word2vec_path):
		self.model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_path, binary=True)
		self.model.init_sims(replace=True)
		self.dimensions = self.model.vector_size

	def get_vector(self, word):
		if word not in self.model.vocab:
			return None
		return self.model.syn0norm[self.model.vocab[word].index]

	def get_similarity(self, word1, word2):
		if word1 not in self.model.vocab or word2 not in self.model.vocab:
			return None
		return self.model.similarity(word1, word2)


if (__name__ == "__main__"):
	model = w2v()
	model.load(r"C:\Users\langh\Datasets\sbw_vectors.bin")
	vec = model.get_vector("hola")
	print(vec)
