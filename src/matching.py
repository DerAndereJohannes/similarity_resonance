from typing import Tuple


def match_single(simr: dict) -> dict:
    m1s, m2s = get_activities_sets(simr.keys())
    high_values = sorted(simr, key=simr.get, reverse=True)
    final_matches = {}
    for key in high_values:
        if key[0] in m1s and key[1] in m2s:
            final_matches[key] = simr[key]
            m1s.remove(key[0])
            m2s.remove(key[1])
        if not m1s and not m2s:
            break

    return final_matches


def get_activities_sets(matches: list) -> Tuple[list, list]:
    model1_set = set()
    model2_set = set()

    for match in matches:
        model1_set.add(match[0])
        model2_set.add(match[1])

    return model1_set, model2_set
