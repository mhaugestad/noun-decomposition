from scipy.stats import gmean
from itertools import chain
from gensim.models import KeyedVectors
from .models import DecompoundingModel
import re
import typing as t

#https://aclanthology.org/N16-1075/

#w2v_model = KeyedVectors.load_word2vec_format('./model.bin', binary=True)

class Decomposition:
    
    def __init__(self, word: str, model: DecompoundingModel, ml: int = 3) -> None:
        # Attach inputs to class instance
        self.word: str = word
        self.ml: int = ml
        self.model = model
        self.compounds = None

        self.similar_candidates = model.get_similar_candidates(self.word)
        self.extended_similar_candidates = model.get_extended_similar_candidates(self.similar_candidates, self.word)
        self.generated_dictionary = list([x for x in model.word_counts.keys() if x in self.word]) # Pre-computed

        self.methods = []

        # Loop through this for each candidate set:
        for method_name, candidates in [#('similar candidates', self.similar_candidates), 
                                        #('extended similar candidates',self.extended_similar_candidates),
                                        ('generated dictionary', self.generated_dictionary)
                                       ]:
                        
            # Produce all spans that corresponds to a match in the distributional thesaurus ie [(0,4),(0,5),(0,6)...]
            candidate_spans: t.List[t.Tuple[int, int]] = [(i,j) for i in range(word.__len__()) for j in range(i+1, word.__len__()+1) if word[i:j] in candidates]
            
            # Deduplicate the candidates using a set: {bund, bunde, bundes, finanz, minister, ministerium}
            candidate_matches: set = {self.word[i:j] for i,j in candidate_spans for x in candidate_spans}

            # Produce all split candidates by adding the end of each candidate span. 
            # Hardcode in a 0 at the beginning. Put in list so can be indexed.
            # ie [0, 4, 5, 6, 9, 12, 20]
            splits: t.List[int] = list(chain.from_iterable(candidate_spans + [(0, len(self.word))]))
            splits = list(set(splits))
            splits.sort()

            method = Method(name=method_name, candidate_spans=candidate_spans, candidates=candidate_matches, splits=splits, ml=self.ml)
            self.methods.append(method)

    def decompose(self) -> t.List[str]:
        """
        Returns a list of tokens
        """
        self.get_compounds()
        return self.compounds[0].resolve()

    
    def get_compounds(self) -> None:
        self.compounds: t.List[Compounds] = []
        for method in self.methods:
            self.compounds.extend([
            Compounds(method.name, [Compound((i,j), self.word, self.model) for i,j in zip(method.suffix_prefix, method.suffix_prefix[1:] + [max(method.splits)])]),
            Compounds(method.name, [Compound((i,j), self.word, self.model) for i,j in zip(method.prefix_suffix, method.prefix_suffix[1:] + [max(method.splits)])])
            ])
        self.compounds: t.List[Compounds] = sorted(self.compounds, key=lambda c: c.score, reverse=True)
        return self

    def __repr__(self):
        if self.compounds:
            return f"Decomposition(word={self.word}, compounds = {self.compounds[0].resolve()})"
        else:
            return f"Decomposition(word={self.word})"

class Compound:
    """
        Class primarily to store probability associated with the compound.
    """
    def __init__(self, span, word, model):
        self.span = span
        self.start = span[0]
        self.end = span[1]
        self.word = word
        self.compound = word[self.start:self.end]
        self.probability = model.get(self.compound)

    def __repr__(self):
        return f"Compound({self.compound}, p={self.probability})"

class Compounds:
    """
        Class to calculate the joint probability of a list of compounds
    """
    def __init__(self, name: str, compounds: list):
        self.name = name
        self.compounds = compounds
        self.score = gmean([c.probability for c in self.compounds])
    
    def resolve(self):
        return [c.compound for c in self.compounds]
    
    def __repr__(self):
        return f"Compounds({self.name}, {','.join([c.compound for c in self.compounds])}, p={self.score})"


class Method:
    def __init__(self, name, candidate_spans, candidates, splits, ml):
        self.name = name
        self.candidate_spans = candidate_spans
        self.candidates = candidates
        self.splits = splits
        self.ml = ml

        self.suffix_prefix: t.List[int] = self.merge_suffix(self.splits)
        self.suffix_prefix: t.List[int] = self.merge_prefix(self.suffix_prefix)

        self.prefix_suffix: t.List[int] = self.merge_prefix(self.splits)
        self.prefix_suffix: t.List[int] = self.merge_suffix(self.prefix_suffix)
    
    def merge_suffix(self, splits) -> t.List[int]:
        """
        Takes a set of indices for splits as input. 
        Produces tuples using zip; (start, start_next)
        """
        merged_splits: t.List[int] = [start for start, start_next in zip(splits, splits[1:] + [max(splits)]) if (start_next - start) > self.ml]
        return merged_splits
    
    def merge_prefix(self, splits) -> t.List[int]:
        """
        Takes a set of indices for splits as input. 
        Produces tuples using zip; (start, start_next.
        """
        merged_splits: t.List[int] = [0] + [start_next for start, start_next in zip(splits, splits[1:]) if (start_next - start) > self.ml]
        return merged_splits

    def __repr__(self):
        return f"Method({self.name})"