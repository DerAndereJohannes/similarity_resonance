from similarity_resonance.src.k_nearest_neighbours import algorithm as knn
from similarity_resonance.src.k_resonance_graph import algorithm as krg
from similarity_resonance.src.iteration import algorithm as it
from similarity_resonance.src.clean_model import clean_transitions
from pm4py.objects.petri.petrinet import PetriNet, Marking
from typing import Tuple


def apply(model1: Tuple[PetriNet, Marking, Marking],
          model2: Tuple[PetriNet, Marking, Marking],
          siml: dict, a: float, k: int, l_thresh: float) -> dict:
    """Similarity Resonance Algorithm. Main goal of finding the similarity
    values between model 1 and model 2 for activity matching algorithms.

    Args:
          model1 (Tuple[PetriNet, Marking, Marking]): Petri Net 1.
          model2 (Tuple[PetriNet, Marking, Marking]): Petri Net 2.
          siml (dict(Tuple[str, str] -> float)): Initial Label Similarity
          Result between both models.
          a (float): Parameter which defines what ratio of the end result
          should be influenced by similarity resonance.
          k (int): Granularity of neighbourhood. Radius of what should be
                considered a neighbour of an activity.
          l_thresh (float): Likelihood threshold to define what is a good
                match.

    Returns:
          dict (Tuple[str, str] -> float): Similarity Resonance vector.
    """

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
