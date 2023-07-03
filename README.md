# SECOS
This repo is a modular python implementation of the SECOS algorithm for decomposing composite nouns.

Based on the SECOS algorithm:

[original implementation](https://github.com/riedlma/SECOS)

[original paper](https://www.inf.uni-hamburg.de/en/inst/ab/lt/publications/2016-riedletal-naacl.pdf)

# Installation

## From Github
`pip install git+https://github.com/mhaugestad/noun-decomposition.git -U`

## From Source
```
git clone
cd noun-decomposition
pip install -e . -U
```

## From Pip
TBC

## Installing models:
The module relies on pretrained models to be passed in. These can be downloaded from command line as follows:

`python -m Secos download --model german`

Or from a python script or notebook like this:

```
from Secos import Decomposition

Decomposition.download_model('german')
```

# Basic Usage
```
from Secos import Decomposition

model = Decomposition.load_model('german')

secos = Decomposition(model)

secos.decompose("Bundesfinanzministerium")

['Bundes', 'finanz', 'ministerium']
```

# Module structure

The code is structured as following:

The entrypoint of the module is the Decomposition class. This class is initialised with an instance of the DecompoundingModel class.

Decomposition relies on two other classes defined in the same script, Compound and Compounds. The compound class keeps track of each compound, its span within the word and its probability of occuring given the precomputed model passed in to the class instance. The Compounds class takes a list of instances of the Compound class, and keeps track of the geometric mean of the whole sequence of Compounds passed to it. This way, during the decomposition we can pull out the sequence of compounds with the highest geometric mean.

# Evaluation