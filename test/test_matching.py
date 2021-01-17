import pytest
from collections import Counter
from pm4py.objects.petri.importer import importer as pnml_importer
from similarity_resonance.src.similarity_resonance import apply
from similarity_resonance.src.matching import match_single, get_activities_sets


class Test_Matching:

    @pytest.fixture
    def simres_result(self):
        k = 1
        l_thresh = 0.2
        a = 0.3
        pn1 = pnml_importer.apply('test_objects/pm1.pnml')
        pn2 = pnml_importer.apply('test_objects/pm2.pnml')
        result = apply(pn1, pn2, a, k, l_thresh)

        return result

    @pytest.fixture
    def matching_activities(self):
        k = 1
        l_thresh = 0.2
        a = 0.3
        pn1 = pnml_importer.apply('test_objects/pm1.pnml')
        pn2 = pnml_importer.apply('test_objects/pm2.pnml')
        result = apply(pn1, pn2, a, k, l_thresh)

        return result.keys()

    def test_matching_activities(self, matching_activities):
        set1, set2 = get_activities_sets(matching_activities)
        assert len(set1) == len(set2)
        assert len(set1) == 7
        assert '' not in set1
        assert '' not in set2

    def test_simres_simple_match(self, simres_result):
        matched_labels = match_single(simres_result)
        assert 1.0 in matched_labels.values()
        assert len(matched_labels) == 7

        list_of_activities_1 = []
        list_of_activities_2 = []
        for result in matched_labels.keys():
            list_of_activities_1.append(result[0])
            list_of_activities_2.append(result[1])

        assert max(Counter(list_of_activities_1).values()) == 1
        assert max(Counter(list_of_activities_2).values()) == 1
