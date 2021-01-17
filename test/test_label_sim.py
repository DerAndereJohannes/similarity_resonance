import pytest
from pm4py.objects.petri.importer import importer as pnml_importer
from simres.src.label_sim import algorithm as labelsim


class Test_LabelSim:

    @pytest.fixture
    def model_indep(self):
        petri_net, *_ = pnml_importer.apply('test_objects/figure1.pnml')
        return petri_net

    @pytest.fixture
    def model_1(self):
        petri_net, *_ = pnml_importer.apply('test_objects/pm1.pnml')
        return petri_net

    @pytest.fixture
    def model_2(self):
        petri_net, *_ = pnml_importer.apply('test_objects/pm2.pnml')
        return petri_net

    @pytest.fixture
    def model_3(self):
        petri_net, im, fm = pnml_importer.apply('test_objects/bc1.pnml')
        return (petri_net, im, fm)

    @pytest.fixture
    def model_4(self):
        petri_net, im, fm = pnml_importer.apply('test_objects/bc2.pnml')
        return (petri_net, im, fm)

    def test_labelsim_spacy_double(self, model_1, model_2):
        siml = labelsim(model_1, model_2)
        assert isinstance(siml, dict)
        assert len(siml.keys()) == 49
        assert siml['Get on Train', 'start'] == 0.6024283617220695
        assert siml['start', 'start'] == 1.0
        assert siml['Enter Barrier', 'Enter Train'] == 0.6230753311102485

    def test_labelsim_spacy_invis_transitions(self, model_3, model_4):
        siml = labelsim(model_3[0], model_4[0])
        assert isinstance(siml, dict)
        assert len(siml.keys()) == 500
