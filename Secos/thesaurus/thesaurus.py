from importlib_resources import files

class DistributionalThesaurus:
    def __init__(self, language: str, distributional_thesaurus, epsilon=0.001):
        """
        Might make sense for performance to create a class for the distributional thesaurus 
        to calculate the number of words and total wordcount up front so we don't have to do it on the fly.

        Any performance to be gained by making a hashed table?
        """
        self.distributional_thesaurus = distributional_thesaurus
        self.n_words = self.distributional_thesaurus.keys().__len__()
        self.total_wordcount = sum(self.distributional_thesaurus.values())
        self.wordset = set(self.distributional_thesaurus.keys())
        self.epsilon = epsilon
        self.language = language
    
    def get(self, __name):
        return self.calculate_probability(__name)

    def calculate_probability(self, __name):
        prob = (self.distributional_thesaurus.get(__name, 0) + self.epsilon) / (self.total_wordcount + self.epsilon * self.n_words)
        return prob
    
    def __repr__(self):
        return f"DistributionalThesaurus({self.language}, n_words={self.n_words}, total_wordcount={self.total_wordcount}, epsilon={self.epsilon})"
    

file = files('Secos.thesaurus').joinpath('denews70M_trigram__WordCount')
with open(file, 'r') as f:
    d = {}
    for line in f.read().splitlines():
        k,v = line.split('\t')
        if all([int(v) >= 50, len(k) >= 5]):
            d[k] = int(v)

german_model = DistributionalThesaurus('German', d)