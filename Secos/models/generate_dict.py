from gensim.models import KeyedVectors
import re
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map, process_map
import pickle

w2v_model = KeyedVectors.load_word2vec_format('./model.bin', binary=True)

def filter_non_alpha(x):
    nonnalphachars = re.findall(r'[^A-Za-z\-]', x)
    return not bool(nonnalphachars)

with open('./denews70M_trigram__WordCount.txt', 'r') as f:
    d = {}
    for line in f.read().splitlines():
        k,v = line.split('\t')
        if all([int(v) >= 50, len(k) >= 5, filter_non_alpha(k)]):
            d[k] = int(v)

def get_similar_candidates(word):
    if word.lower() in w2v_model:
        similar_candidates = list(map(lambda x: x[0], w2v_model.similar_by_word(word.lower(), 200)))
        similar_candidates = list(filter(lambda x: x in word, similar_candidates))
        return similar_candidates
    else:
        return []

if __name__ == '__main__':
    generated_dictionary = process_map(get_similar_candidates, list(d.keys()), chunksize=1000, max_workers = 4)
    with open('filename.pickle', 'wb') as f:
        pickle.dump(generated_dictionary, f)