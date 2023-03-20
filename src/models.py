from scipy.stats import gmean
import re
import typing as t

#https://aclanthology.org/N16-1075/

class Term:
    def __init__(self, span: tuple, word: str, distributional_thesaurus):
        """
        """
        self.span: tuple = span
        self.start, self.end = span
        self.word: str = word
        self.term: str = word[self.start:self.end]
        self.distributional_thesaurus: dict = distributional_thesaurus
        self.oov: bool = self.term in distributional_thesaurus.keys()
        self.frequency: int = distributional_thesaurus.get(self.term, 0)
        self.prefix: Term | None = None
        self.suffix: Term | None = None
        self.children: t.List[Term|None] = []
    
    def __bool__(self):
        """
        Used for filtering out out-of-vocabulary words.
        Helps to make the function to get all candidates more succinct.
        """
        return self.oov

    def __gt__(self, other):
        """
        """
        return self.end >= other.start

    def paths(self):
        """
            Recursive Tree / Graph traverals to find all valid paths of candidate terms through a word
        """
        if not self.children:
            return [[self]]
        paths = []
        for child in self.children:
            for path in child.paths():
                paths.append([self] + path)
        return paths

    def __repr__(self):
        return f"Term({self.term}, {self.start}, {self.end})"

class Prefix(Term):
    def __repr__(self):
        return f"Prefix({self.term}, {self.start}, {self.end})"

class Suffix(Term):
    def __repr__(self):
        return f"Suffix({self.term}, {self.start}, {self.end})"

class Word:
    def __init__(self, word: str, distributional_thesaurus: dict, ml=3):
        """
        ml: minimum length for merging
        """
        self.word: str = word
        self.total_wordcount: int = sum(distributional_thesaurus.values())
        self.n_words: int = len(distributional_thesaurus.keys())
        candidates: t.List[Term] = get_candidates(word.lower(), distributional_thesaurus) # German is case sensitive - should be parametrized.
        self.candidates: t.List[Term] = sorted(candidates, key=lambda x: x.span)
        #split_possibilities = []
        #Candidates(candidates, word, distributional_thesaurus, self.n_words, self.total_wordcount)

    def split(self):
        tokens = sorted(list(zip(self.tokens.splits, self.tokens.scores)), key=lambda x: x[1], reverse=True)
        if tokens:
            return [x.term for x in tokens[0][0]]
        else:
            return [self.word]
        
    def __repr__(self):
        return f"Word('{self.word}')"


#similar candidate units

class Candidates:
    def __init__(self, spans: list, word: str, distributional_thesaurus: dict, n_words: int, total_wordcount: int):
        self.n_words = n_words
        self.total_wordcount = total_wordcount
        self.spans = sorted(spans, key=lambda x: x.span)
        for span in spans:
            span.children = get_next(span, self)
        
        # self.splits = [[Term((0, word.__len__()), word, distributional_thesaurus)]]
        # for span in [s for s in spans if s.start ==0]:
        #     paths = span.paths()
        #     print(paths)
        #     paths = list(filter(lambda term: any([tok.frequency for tok in term]), paths))
        #     self.splits.extend(paths)
        # self.scorer(epsilon=0.01)
    
    def scorer(self, epsilon=0.01):
        self.scores = []
        for split in self.splits:
            self.scores.append(gmean([(w.frequency + epsilon) / ((self.total_wordcount + epsilon) * self.n_words) for w in split]))
        return None
    
    def __repr__(self):
        return f"Candidates({self.spans})"

def get_candidates(word, distributional_thesaurus):
    all_candidates = set(
        Term((i,j), word, distributional_thesaurus ) for i in range(word.__len__()) for j in range(i+1, word.__len__()+1)
    )
    return list(filter(None, all_candidates))

def get_next(term: Term, candidates: t.List[Term]):
    idx = candidates.index(term)
    if idx < len(candidates):
        successors = [w for w in candidates[idx:] if candidates[idx].end <= w.start]
        if successors:
            minx = min(successors, key=lambda x: x.start).start
            return [x for x in successors if x.start == minx]
        return successors
    else:
        return []

