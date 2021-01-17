import pytest
from pm4py.objects.petri.importer import importer as pnml_importer
from simres.src.similarity_resonance import apply


class Test_SimilarityResonance:

    @pytest.fixture
    def input1(self):
        k = 1
        l_thresh = 0.2
        a = 0.3
        pn1 = pnml_importer.apply('test_objects/pm1.pnml')
        pn2 = pnml_importer.apply('test_objects/pm2.pnml')

        return pn1, pn2, a, k, l_thresh

    def test_simres_simple(self, input1):
        result = apply(input1[0], input1[1], input1[2], input1[3], input1[4])
        assert len(result.keys()) == 49
        assert 1.0 in result.values()
        assert round(
            result[('Read Newspaper', 'Browse News on Phone')], 2) == 0.48
