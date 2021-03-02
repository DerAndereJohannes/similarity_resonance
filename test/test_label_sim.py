import os
import pytest
from pm4py.objects.petri.importer import importer as pnml_importer
from similarity_resonance.src.label_sim import algorithm as labelsim


class Test_LabelSim:

    @pytest.fixture
    def model_indep(self):
        cd = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(cd, 'test_objects/figure1.pnml')
        petri_net, *_ = pnml_importer.apply(model_path)
        return petri_net

    @pytest.fixture
    def model_1(self):
        cd = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(cd, 'test_objects/pm1.pnml')
        petri_net, *_ = pnml_importer.apply(model_path)
        return petri_net

    @pytest.fixture
    def model_2(self):
        cd = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(cd, 'test_objects/pm2.pnml')
        petri_net, *_ = pnml_importer.apply(model_path)
        return petri_net

    @pytest.fixture
    def model_3(self):
        cd = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(cd, 'test_objects/bc1.pnml')
        petri_net, *_ = pnml_importer.apply(model_path)
        return petri_net

    @pytest.fixture
    def model_4(self):
        cd = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(cd, 'test_objects/bc2.pnml')
        petri_net, *_ = pnml_importer.apply(model_path)
        return petri_net

    def test_labelsim_spacy_double(self, model_1, model_2):
        siml = labelsim(model_1, model_2)
        assert isinstance(siml, dict)
        assert len(siml.keys()) == 49
        assert round(siml['Get on Train', 'start'], 3) == 0.602
        assert siml['start', 'start'] == 1.0
        assert round(siml['Enter Barrier', 'Enter Train'], 3) == 0.623

    def test_labelsim_spacy_invis_transitions(self, model_3, model_4):
        siml = labelsim(model_3, model_4)
        assert isinstance(siml, dict)
        assert len(siml.keys()) == 500
