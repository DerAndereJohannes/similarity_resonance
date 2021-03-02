from typing import Tuple


def match_single(simr: dict) -> dict:
    """Sort the dictionary by descending value and iterate through and match
    the top pairs with each other until every activity from model 1 has found
    the best match in model 2. (One-to-One matching)

    Args:
        simr (dict): Similarity Resonance vector.

    Returns:
        dict: Dictionary of the best matches from model 1 to model 2 with their
            final similarity scores.
    """
    m1s, m2s = get_activities_sets(simr.keys())
    high_values = sorted(simr, key=simr.get, reverse=True)
    final_matches = {}
    for key in high_values:
        if key[0] in m1s and key[1] in m2s:
            final_matches[key] = simr[key]
            m1s.remove(key[0])
            m2s.remove(key[1])
        if not m1s or not m2s:
            break

    return final_matches


def get_activities_sets(matches: list) -> Tuple[set, set]:
    """Get the transition / activity labels from both models.

    Args:
        matches (list): list of Tuple[str, str] containing all labels.

    Returns:
        Tuple[set, set]: Sets containing all activity / transition labels of
            both models
    """
    model1_set = set()
    model2_set = set()

    for match in matches:
        model1_set.add(match[0])
        model2_set.add(match[1])

    return model1_set, model2_set
