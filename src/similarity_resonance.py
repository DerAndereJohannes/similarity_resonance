from similarity_resonance.src.k_nearest_neighbours import algorithm as knn
from similarity_resonance.src.k_resonance_graph import algorithm as krg
from similarity_resonance.src.iteration import algorithm as it
from similarity_resonance.src.label_sim import algorithm as label_sim
from pm4py.objects.petri.petrinet import PetriNet, Marking
from typing import Tuple


def apply(model1: Tuple[PetriNet, Marking, Marking],
          model2: Tuple[PetriNet, Marking, Marking],
          a: float, k: int, l_thresh: float) -> dict:

    siml = label_sim(model1[0], model2[0])
    knn_result = knn(model1, model2, k)
    krg_result = krg(siml, knn_result, l_thresh)
    result = it(siml, krg_result, a)

    return result
