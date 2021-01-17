from pm4py.objects.petri.petrinet import PetriNet, Marking
from similarity_resonance.src.objects.knn_node import KnnNode
from pm4py.algo.discovery.footprints import algorithm as footprint_discovery
from typing import Tuple


def algorithm(model1: Tuple[PetriNet, Marking, Marking],
              model2: Tuple[PetriNet, Marking, Marking],
              k: int) -> Tuple[list, list]:

    footprints1 = footprint_discovery.apply(model1[0], model1[1])
    footprints2 = footprint_discovery.apply(model2[0], model2[1])

    knn1 = get_complete_knn(footprints1, k)
    knn2 = get_complete_knn(footprints2, k)

    return knn1, knn2


def get_complete_knn(model: dict, k: int) -> list:
    knn_result = []
    for activity in model['activities']:
        knn_result.append(
            compute_activity_knn(list(model['sequence']), activity, k))

    return knn_result


def compute_activity_knn(model: list, activity: str, k: int) -> KnnNode:
    new_node = KnnNode(activity)
    new_node.set_preset(get_preset_knn(model, activity, k))
    new_node.set_postset(get_postset_knn(model, activity, k))

    return new_node


def get_postset_knn(model: list, activity: str, k: int) -> list:
    new_postset = []
    current_activity = [activity]
    next_activity = []
    for _ in range(1, k+1):
        for seq in model:
            if seq[0] in current_activity and seq[1].strip() != '':
                new_postset.append(seq[1])
                next_activity.append(seq[1])
        current_activity = next_activity
        next_activity = []

    return new_postset


def get_preset_knn(model: list, activity: str, k: int) -> list:
    new_preset = []
    current_activity = [activity]
    next_activity = []
    for _ in range(1, k+1):
        for seq in model:
            if seq[1] in current_activity and seq[0].strip() != '':
                new_preset.append(seq[0])
                next_activity.append(seq[0])
        current_activity = next_activity
        next_activity = []

    return new_preset
