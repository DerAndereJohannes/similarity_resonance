import os
import pytest
from pm4py.objects.petri.importer import importer as pnml_importer
from similarity_resonance.src.similarity_resonance import apply
from similarity_resonance.test.test_objects.siml import pm1_pm2_siml


class Test_SimilarityResonance:

    @pytest.fixture
    def input1(self):
        cd = os.path.dirname(os.path.realpath(__file__))
        model_path1 = os.path.join(cd, 'test_objects/pm1.pnml')
        model_path2 = os.path.join(cd, 'test_objects/pm2.pnml')
        k = 1
        l_thresh = 0.2
        a = 0.3
        pn1 = pnml_importer.apply(model_path1)
        pn2 = pnml_importer.apply(model_path2)
        siml = pm1_pm2_siml

        return pn1, pn2, siml, a, k, l_thresh

    def test_simres_simple(self, input1):
        result = apply(input1[0], input1[1], input1[2],
                       input1[3], input1[4], input1[5])
        assert len(result.keys()) == 49
        assert 1.0 in result.values()
        assert round(
            result[('Read Newspaper', 'Browse News on Phone')], 2) == 0.65
