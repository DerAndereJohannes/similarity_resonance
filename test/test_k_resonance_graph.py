import pytest
from pm4py.objects.petri.importer import importer as pnml_importer
import simres.src.k_resonance_graph as krg
from simres.src.objects.krg_node import KrgNode
from simres.src.label_sim import algorithm as labelsim
from simres.src.k_nearest_neighbours import algorithm as knn


class Test_KResonanceGraph:

    @pytest.fixture
    def input_1(self):
        k = 1
        l_thresh = 0.2
        pn1 = pnml_importer.apply('test_objects/pm1.pnml')
        pn2 = pnml_importer.apply('test_objects/pm2.pnml')
        siml = labelsim(pn1[0], pn2[0])
        knn_result = knn(pn1, pn2, k)
        return siml, knn_result, l_thresh

    def test_krg_lmax(self, input_1):
        lmax = krg.get_LMAX(krg.get_L1(input_1[0]), krg.get_L2(input_1[0]))
        assert round(lmax[('Enter Barrier', 'Exit Train')], 3) == 0.125
        assert round(lmax[('start', 'start')], 3) == 0.269
        assert lmax[('start', 'Pass Barrier (1)')] == lmax[
            ('start', 'Pass Barrier (2)')]

    def test_krg_generation(self, input_1):
        krg_result = krg.algorithm(input_1[0], input_1[1], input_1[2])

        assert len(krg_result) == len(input_1[0])
        for m in krg_result:
            assert isinstance(m, KrgNode)
            if m.activity_set == ('Read Newspaper', 'Browse News on Phone'):
                assert m.pre_set == {('Get on Train', 'Enter Train'): (5/6)}
                assert m.post_set == {('Get off Train', 'Exit Train'): (1/6)}

            if m.pre_set or m.post_set:
                pre_values = sum(m.pre_set.values())
                post_values = sum(m.post_set.values())
                combined = pre_values + post_values
                assert abs(combined-1.0) < 0.0001
