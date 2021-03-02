from pm4py.objects.petri.petrinet import PetriNet, Marking
from similarity_resonance.src.objects.knn_node import KnnNode
from pm4py.algo.discovery.footprints import algorithm as footprint_discovery
from typing import Tuple


def algorithm(model1: Tuple[PetriNet, Marking, Marking],
              model2: Tuple[PetriNet, Marking, Marking],
              k: int) -> Tuple[list, list]:
    """K-Nearest Neighbours. For each input model, find all the neighbours of
    all of the activities with a granularity parameter of k.

    Args:
        model1 (Tuple[PetriNet, Marking, Marking]): Petri net 1.
        model2 (Tuple[PetriNet, Marking, Marking]): Petri net 2.
        k (int): Granularity parameter. ie. Radius of activity neighbourhood

    Returns:
        Tuple[list, list]: List of KNN nodes for each model.
    """

    footprints1 = footprint_discovery.apply(model1[0], model1[1])
    footprints2 = footprint_discovery.apply(model2[0], model2[1])

    knn1 = get_complete_knn(footprints1, k)
    knn2 = get_complete_knn(footprints2, k)

    return knn1, knn2


def get_complete_knn(model: dict, k: int) -> list:
    """Calculates all KNN nodes of a petri net. Iterates through all activities
    and generates a KNN node for each with granularity level of k.

    Args:
        model (dict): Input footprint matrix result
        k (int): Granularity parameter. ir. Radius of activity neighbourhood.

    Returns:
        list: KNN representation of a petri net.
    """
    knn_result = []
    for activity in model['activities']:
        knn_result.append(
            compute_activity_knn(list(model['sequence']), activity, k))

    return knn_result


def compute_activity_knn(model: list, activity: str, k: int) -> KnnNode:
    """Calculates the pre and post set of an activity in a petri net.

    Args:
        model (list): List of sequence transitions in footprint matrix.
        activity (str): Activity label to get neighbourhood of.
        k (int): Granularity parameter.

    Returns:
        KnnNode: KNN node representation of given activity string of the model.
    """
    new_node = KnnNode(activity)
    new_node.set_preset(get_preset_knn(model, activity, k))
    new_node.set_postset(get_postset_knn(model, activity, k))

    return new_node


def get_postset_knn(model: list, activity: str, k: int) -> list:
    """Calculate the post set of the activity label in the petri net.

    Args:
        model (list): List of sequence transitions in footprint matrix.
        activity (str): Activity label to get neighbourhood of.
        k (int): Granularity parameter.

    Returns:
        list: List of neighbours ahead of the target activity.
    """
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
    """Calculate the pre set of the activity label in the petri net.

    Args:
        model (list): List of sequence transitions in footprint matrix.
        activity (str): Activity label to get neighbourhood of.
        k (int): Granularity parameter.

    Returns:
        list: List of neighbours behind of the target activity.
    """
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
