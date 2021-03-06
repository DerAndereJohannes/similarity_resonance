import os
import pytest
from collections import Counter
from pm4py.objects.petri.importer import importer as pnml_importer
from similarity_resonance.src.similarity_resonance import apply
from similarity_resonance.src.matching import match_single, get_activities_sets
from similarity_resonance.test.test_objects.siml import pm1_pm2_siml


class Test_Matching:

    @pytest.fixture
    def simres_result(self):
        cd = os.path.dirname(os.path.realpath(__file__))
        model_path1 = os.path.join(cd, 'test_objects/pm1.pnml')
        model_path2 = os.path.join(cd, 'test_objects/pm2.pnml')
        k = 1
        l_thresh = 0.2
        a = 0.3
        pn1 = pnml_importer.apply(model_path1)
        pn2 = pnml_importer.apply(model_path2)
        siml = pm1_pm2_siml
        result = apply(pn1, pn2, siml, a, k, l_thresh)

        return result

    @pytest.fixture
    def matching_activities(self):
        cd = os.path.dirname(os.path.realpath(__file__))
        model_path1 = os.path.join(cd, 'test_objects/pm1.pnml')
        model_path2 = os.path.join(cd, 'test_objects/pm2.pnml')
        k = 1
        l_thresh = 0.2
        a = 0.3
        pn1 = pnml_importer.apply(model_path1)
        pn2 = pnml_importer.apply(model_path2)
        siml = pm1_pm2_siml
        result = apply(pn1, pn2, siml, a, k, l_thresh)

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
