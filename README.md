# Similarity Resonance: Python Implementation
[![Build Status](https://cloud.drone.io/api/badges/DerAndereJohannes/similarity_resonance/status.svg)](https://cloud.drone.io/DerAndereJohannes/similarity_resonance)
## Introduction
This github repository consists of a python implementation of the 'Similarity Resonance' concept for matching activities in two process models. The goal of the algorithm is to extend the notion of label similarities and to compliment it with a global contextual similarity. The original paper and idea was authored by Nour Assy, Boudewijn F. van Dongen and Wil M.P van der Aalst at the Technical University of Eindhoven. For reference of the theory, please [take a look at the original paper (link)](https://dl.acm.org/doi/10.1145/3167132.3167138). Alternatively, you can check out the presentation slides that the author used [here (PDF download)](https://pa.win.tue.nl/wp-content/uploads/2018/09/2017_assy-october.pdf)

## Installation
The algorithm was developed on Python 3.9. The provided requirements.txt pip file can be used to install all the dependencies required for the program to work. I would suggest to install this in a virtual environment. The main dependencies are:
- pm4py
- flake8
- pytest
- pytest-cov

Optional:
To get an initial label similarity value for testing, the package SpaCy was used. These dependencies are quite large (700MB+) and are therefore in a separate file (requirements_spacy.txt). If you plan to use this package, then install it too. If you are looking to use your own initial similarity measurement, make sure to make the siml output in format of a dictionary where key: Tuple[str, str] -> value: float.

Make sure to place the downloaded repository into the environment's python site-packages folder. (eg. /usr/local/anaconda3/envs/myenv/lib/python3.9/site-packages/)

**WARNING:** To compute the initial label similarity, I have chosen to use spacy along with the large model. This will take some time to download. Installing through the requirements.txt file will automatically download the additional module. If manually installing the dependencies, make sure to also get this module from [here.](https://spacy.io/models/en)
## Parameters
**model1:** Source model (Petri Net)

**model2:** Target model (Petri Net)

**siml:** Initial label similarity values (Dictionary | key: Tuple[str, str] -> float)

**a:** defines how much the similarity value should rely on the global contextual similarity. 0 is not at all, 1.0 is all of it. a ∈ [0, 1]

**k:** defines the distance from transition that should be considered a neighbour.  k ∈ N+

**l_thresh:** defines the match likelihood ratio threshold to be considered similar. l_thresh ∈ [0, 1]
## Usage Example
```python
import pm4py
from similarity_resonance.src.label_sim import algorithm as label_sim
from similarity_resonance.src.similarity_resonance import apply as sim_res
from similarity_resonance.src.matching import match_single

petri1 = pm4py.read_petri_net('link/to/petri/net/1')
petri2 = pm4py.read_petri_net('link/to/petri/net/2')
siml = label_sim(petri1[0], petri2[0])

similarity_values = sim_res(petri1, petri2, siml, a=0.3, k=2, l_thresh=0.2)
top_matches = match_single(similarity_values)

for key, value in top_matches.items():
    print(key, value)

```