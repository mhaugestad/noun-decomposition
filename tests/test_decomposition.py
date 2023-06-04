# content of test_sysexit.py
import pytest
from Secos.Decomposition import Decomposition
from Secos.models import DecompoundingModel

model = DecompoundingModel(
    language='German',
    precomputed_splits={},
    generated_dictionary=dict(zip(['Bund', 'Bunde', 'Bundes','finanz', 'minister', 'ministerium'], [1,1,1,1, 1, 1])),
    total_wordcount=100,
    n_words = 4,
    ml=3,
)

secos = Decomposition(model=model)

def test_splits():
    word = 'Bundesfinanzministerium'
    computed_splits = secos.get_possible_splits(word)
    defined_splits = [0, 4, 5, 6, 12, 20, 23]
    assert defined_splits == computed_splits

def test_splits():
    word = 'Bundesfinanzministerium'
    computed_splits = secos.get_possible_splits(word)
    defined_splits = [0, 4, 5, 6, 12, 20, 23]
    assert defined_splits == computed_splits


def test_probability_score():
    calculated_probability = model.calculate_probability('Bund')
    actual_probability = (1 + 0.001) / (100 + 0.001 * 4)
    assert actual_probability == calculated_probability