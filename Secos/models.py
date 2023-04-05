from scipy.stats import gmean
from .thesaurus import DistributionalThesaurus
import re
import typing as t

#https://aclanthology.org/N16-1075/

class Decomposition:
    def __init__(self, word: str, distributional_thesaurus: DistributionalThesaurus, ml: int = 3) -> None:
        # Attach inputs to class instance
        self.word: str = word
        self.ml: int = ml
        self.distributional_thesaurus: DistributionalThesaurus = distributional_thesaurus
        self.compounds = None

        # Produce all spans that corresponds to a match in the distributional thesaurus
        self.candidate_spans: t.List[t.Tuple[int, int]] = [(i,j) for i in range(word.__len__()) for j in range(i+1, word.__len__()+1) if word[i:j] in self.distributional_thesaurus.wordset]
        
        # Deduplicate the candidates using a set
        self.candidates: set = {self.word[i:j] for i,j in self.candidate_spans for x in self.candidate_spans}

        # Produce all split candidates by adding the end of each candidate span. Hardcode in a 0 at the beginning. Put in list so can be indexed.
        self.splits: t.List[int] = list(set( [0] + list(map(lambda x: x[1], self.candidate_spans)) + [len(self.word)] ))
        self.splits.sort()

    def decompose(self) -> t.List[str]:
        """
        Function to perform the character ngram merging and chose the bestr split.
        Returns a list of tokens
        """
        self.suffix_prefix: t.List[int] = self.merge_suffix(self.splits)
        self.suffix_prefix: t.List[int] = self.merge_prefix(self.suffix_prefix)

        self.prefix_suffix: t.List[int] = self.merge_prefix(self.splits)
        self.prefix_suffix: t.List[int] = self.merge_suffix(self.prefix_suffix)

        self.get_compounds()

        return self.compounds[0].resolve()

    def merge_suffix(self, splits) -> t.List[int]:
        """
        Takes a set of indices for splits as input. 
        Produces tuples using zip; (start, start_next.
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
        
    def get_compounds(self) -> None:
        self.compounds: t.List[Compounds] = [
            Compounds([Compound((i,j), self.word, self.distributional_thesaurus) for i,j in zip(self.suffix_prefix, self.suffix_prefix[1:] + [max(self.splits)])]),
            Compounds([Compound((i,j), self.word, self.distributional_thesaurus) for i,j in zip(self.prefix_suffix, self.prefix_suffix[1:] + [max(self.splits)])])
            ]
        self.compounds: t.List[Compounds] = sorted(self.compounds, key=lambda c: c.score, reverse=True)
        return self

    def __repr__(self):
        if self.compounds:
            return f"Decomposition(word={self.word}, compounds = {self.compounds[0].resolve()})"
        else:
            return f"Decomposition(word={self.word})"

class Compound:
    def __init__(self, span, word, distributional_thesaurus):
        self.span = span
        self.start = span[0]
        self.end = span[1]
        self.word = word
        self.compound = word[self.start:self.end]
        self.probability = distributional_thesaurus.get(self.compound)
    
    def __repr__(self):
        return f"Compound({self.compound}, p={self.probability})"

class Compounds:
    def __init__(self, compounds: list):
        self.compounds = compounds
        self.score = gmean([c.probability for c in self.compounds])
    
    def resolve(self):
        return [c.compound for c in self.compounds]
    
    def __repr__(self):
        return f"Compounds({','.join([c.compound for c in self.compounds])}, p={self.score})"