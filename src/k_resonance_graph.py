from similarity_resonance.src.objects.krg_node import KrgNode
from typing import Tuple


def algorithm(siml: dict,
              knn_result: Tuple[list, list], l_thresh: float) -> list:
    """K-Resonance Graph algorithm. Create KRG nodes and outgoing arcs to
    represent the KRG.

    Args:
        siml (dict): Initial label similarity result.
        knn_result (Tuple[list, list]): KNN nodes to use for arcs.
        l_thresh (float): likelihood threshold to define what a good match is.

    Returns:
        list: KRG representation.
    """

    likelihood_factor = get_LMAX(get_L1(siml), get_L2(siml))
    krg_result = generate_krg(siml, knn_result, l_thresh, likelihood_factor)

    return krg_result


def get_L1(siml: dict) -> dict:
    """Calculate the match likelihood comparing over model 1.

    Args:
        siml (dict): Initial label similarity dictionary.

    Returns:
        dict: Dictionary of L1 results.
    """
    l1 = {}
    for key, value in siml.items():
        sum_denominator = value
        for key1, value1 in siml.items():
            if key != key1:
                if key[0] == key1[0]:
                    sum_denominator += value1
        l1[key] = value / sum_denominator

    return l1


def get_L2(siml: dict) -> dict:
    """Calculate the match likelihood comparing over model 2.

    Args:
        siml (dict): Initial label similarity dictionary.

    Returns:
        dict: Dictionary of L2 results.
    """
    l2 = {}
    for key, value in siml.items():
        sum_denominator = value
        for key1, value1 in siml.items():
            if key != key1:
                if key[1] == key1[1]:
                    sum_denominator += value1
        l2[key] = value / sum_denominator

    return l2


def get_LMAX(l1: dict, l2: dict) -> dict:
    """Generate the maximum match likelihood of all matches

    Args:
        l1 (dict): Match likelihood results from L1.
        l2 (dict): Match likelihood results from L2.

    Returns:
        dict: Maximum match likelihood results.
    """
    lmax = {}
    for key, value in l1.items():
        if value >= l2[key]:
            lmax[key] = value
        else:
            lmax[key] = l2[key]

    return lmax


def generate_krg(siml: dict, knn_result: Tuple[list, list],
                 l_thresh: float, lmax: dict) -> list:
    """Generate the KRG graph using the initial label similarity keys as nodes,
    KNN neighbourhoods as outgoing arcs and maximum likelihood matches as arc
    weights.

    Args:
        siml (dict): Initial label similarity dictionary.
        knn_result (Tuple[list, list]): KNN result of both models.
        l_thresh (float): Likelihood threshold to define a good match.
        lmax (dict): Maximum match likelihoods between both models.

    Returns:
        list: KRG representation.
    """

    krg_result = []
    for match_key in siml.keys():
        new_node = KrgNode(match_key)
        knn_src = \
            next((x for x in knn_result[0] if x.activity == match_key[0]),
                 None)
        knn_target = \
            next((x for x in knn_result[1] if x.activity == match_key[1]),
                 None)
        new_node.generate_preset(knn_src, knn_target, lmax, l_thresh)
        new_node.generate_postset(knn_src, knn_target, lmax, l_thresh)
        new_node.compute_edge_weights()

        krg_result.append(new_node)

    return krg_result
