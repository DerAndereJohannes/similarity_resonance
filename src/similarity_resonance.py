from similarity_resonance.src.k_nearest_neighbours import algorithm as knn
from similarity_resonance.src.k_resonance_graph import algorithm as krg
from similarity_resonance.src.iteration import algorithm as it
from similarity_resonance.src.clean_model import clean_transitions
from pm4py.objects.petri.petrinet import PetriNet, Marking
from typing import Tuple


def apply(model1: Tuple[PetriNet, Marking, Marking],
          model2: Tuple[PetriNet, Marking, Marking],
          siml: dict, a: float, k: int, l_thresh: float) -> dict:

    # convert empty labels to invisible transitions
    clean_transitions(model1[0])
    clean_transitions(model2[0])

    # calculate the k nearest neighbours for each activity
    knn_result = knn(model1, model2, k)

    # create the k resonance graph object from previous outputs
    krg_result = krg(siml, knn_result, l_thresh)

    # convert k resonance graph into a power iteration problem and solve
    result = it(siml, krg_result, a)

    return result
