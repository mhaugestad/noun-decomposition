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
pip install noun-decomposition

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

# Evaluation
The evaluation folder includes code for the evaluation of the pretrained models.