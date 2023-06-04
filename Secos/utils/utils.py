from itertools import chain
import typing as t

def get_possible_splits(word, subwords) -> list:
    """
    
    """
    
    # Produce all spans that corresponds to a match in the distributional thesaurus ie [(0,4),(0,5),(0,6)...]
    candidate_spans: t.List[t.Tuple[int, int]] = [(i,j) for i in range(word.__len__()) for j in range(i+1, word.__len__()+1) if word[i:j] in subwords]
            
    # Deduplicate the candidates using a set: {bund, bunde, bundes, finanz, minister, ministerium}
    candidate_matches: set = {word[i:j] for i,j in candidate_spans for x in candidate_spans}

    # Produce all split candidates 
    # Hardcode in a 0 at the beginning. Put in list so can be indexed.
    # ie [0, 4, 5, 6, 9, 12, 20]
    splits: t.List[int] = list(chain.from_iterable(candidate_spans + [(0, len(word))]))
    splits = list(set(splits))
    splits.sort()
    return splits

def merge_suffix(splits, ml) -> t.List[int]:
    """
    Takes a set of indices for splits as input. 
    Produces tuples using zip; (start, start_next)
    """
    merged_splits: t.List[int] = [start for start, start_next in zip(splits, splits[1:] + [max(splits)]) if (start_next - start) > ml]
    return merged_splits
    
def merge_prefix(splits, ml) -> t.List[int]:
    """
    Takes a set of indices for splits as input. 
    Produces tuples using zip; (start, start_next).
    """
    merged_splits: t.List[int] = [0] + [start_next for start, start_next in zip(splits, splits[1:]) if (start_next - start) > ml]
    return merged_splits