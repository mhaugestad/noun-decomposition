from importlib_resources import files
from gensim.models import KeyedVectors

w2v_model = KeyedVectors.load_word2vec_format(files('Secos.models').joinpath('./model.bin'), binary=True)

#https://devmount.github.io/GermanWordEmbeddings/

class DecompoundingModel:
    def __init__(self, language: str, word_counts: dict, similarity_model: KeyedVectors = w2v_model, epsilon=0.001):
        """
        Might make sense for performance to create a class for the distributional thesaurus 
        to calculate the number of words and total wordcount up front so we don't have to do it on the fly.

        Any performance to be gained by making a hashed table?
        """
        self.word_counts = word_counts
        self.n_words = self.word_counts.keys().__len__()
        self.total_wordcount = sum(self.word_counts.values())
        self.generated_dictionary = ...
        self.epsilon = epsilon
        self.language = language
        self.similarity_model = similarity_model
    
    def get(self, __name):
        return self.calculate_probability(__name)

    def calculate_probability(self, __name):
        prob = (self.word_counts.get(__name, 0) + self.epsilon) / (self.total_wordcount + self.epsilon * self.n_words)
        return prob
    
    def get_similar_candidates(self, word, l=200):
        similar_candidates = list(map(lambda x: x[0], self.similarity_model.similar_by_word(word.lower(), l)))
        similar_candidates = list(filter(lambda x: x in word, similar_candidates))
        return similar_candidates
    
    def get_extended_similar_candidates(self, word, similar_candidates, l=200):
        extended_similar_candidates = set()
        for w in similar_candidates:
            similar_candidates = list(map(lambda x: x[0], self.similarity_model.similar_by_word(w.lower(), l)))
            similar_candidates = set(filter(lambda x: x in word, similar_candidates))
            extended_similar_candidates.update(similar_candidates)
        return list(extended_similar_candidates)

    def __repr__(self):
        return f"DecompoundingModel({self.language}, n_words={self.n_words}, total_wordcount={self.total_wordcount}, epsilon={self.epsilon})"
    

file = files('Secos.models').joinpath('denews70M_trigram__WordCount.txt')
with open(file, 'r') as f:
    d = {}
    for line in f.read().splitlines():
        k,v = line.split('\t')
        if all([int(v) >= 50, len(k) >= 5]):
            d[k] = int(v)

german_model = DecompoundingModel('German', d)