import pytest
import similarity_resonance.src.k_nearest_neighbours as knn
from similarity_resonance.src.objects.knn_node import KnnNode
from pm4py.objects.petri.importer import importer as pnml_importer
from pm4py.algo.discovery.footprints import algorithm as footprint_discovery


class Test_KNearestNeighbours:

    @pytest.fixture
    def model_1(self):
        petri_net = pnml_importer.apply('test_objects/pm1.pnml')
        return petri_net

    @pytest.fixture
    def model_2(self):
        petri_net = pnml_importer.apply('test_objects/pm2.pnml')
        return petri_net

    @pytest.mark.parametrize('k,activity,expected',
                             [(1, 'Read Newspaper', ['Get off Train']),
                              (2, 'Read Newspaper',
                               ['Get off Train', 'Exit Barrier'])])
    def test_GetPostSet(self, model_1, activity, k, expected):
        footprint = footprint_discovery.apply(model_1[0], model_1[1])
        sequence = list(footprint['sequence'])
        post_set = knn.get_postset_knn(sequence, activity, k)
        assert post_set == expected

    @pytest.mark.parametrize('k,activity,expected',
                             [(1, 'Read Newspaper', ['Get on Train']),
                              (2, 'Read Newspaper',
                               ['Get on Train', 'Enter Barrier'])])
    def test_GetPreSet(self, model_1, activity, k, expected):
        footprint = footprint_discovery.apply(model_1[0], model_1[1])
        sequence = list(footprint['sequence'])
        pre_set = knn.get_preset_knn(sequence, activity, k)
        assert pre_set == expected

    @pytest.mark.parametrize('k,activity,exp_pre,exp_post',
                             [(1, 'Read Newspaper',
                               ['Get on Train'], ['Get off Train']),
                              (2, 'Read Newspaper',
                               ['Get on Train', 'Enter Barrier'],
                               ['Get off Train', 'Exit Barrier'])])
    def test_knn_object(self, model_1, activity, k, exp_pre, exp_post):
        footprint = footprint_discovery.apply(model_1[0], model_1[1])
        sequence = list(footprint['sequence'])
        new_node = knn.compute_activity_knn(sequence, activity, k)
        assert isinstance(new_node, KnnNode)
        assert new_node.activity == activity
        assert new_node.post_set == exp_post
        assert new_node.pre_set == exp_pre

    @pytest.mark.parametrize('k', [1])
    def test_full_knn(self, model_1, model_2, k):
        knn1, knn2 = knn.algorithm(model_1, model_2, k)
        assert isinstance(knn1, list)
        assert isinstance(knn2, list)
        assert len(knn1) == 7
        assert len(knn2) == 7
        for node1, node2 in zip(knn1, knn2):
            print(node2.activity, node2.pre_set, node2.post_set)
            assert isinstance(node1, KnnNode)
            assert isinstance(node2, KnnNode)
