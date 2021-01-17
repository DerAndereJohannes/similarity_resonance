import spacy
import re
from pm4py.objects.petri.petrinet import PetriNet


def algorithm(model1: PetriNet, model2: PetriNet) -> dict:
    nlp = spacy.load('en_core_web_lg')
    siml = {}
    for transition1 in model1.transitions:
        curr_label = re.sub(r'\([0-9]+\)', '', transition1.label).strip()
        if curr_label != '':
            l1 = nlp(curr_label)
            for transition2 in model2.transitions:
                compare_label = re.sub(r'\([0-9]+\)', '',
                                       transition2.label).strip()
                if compare_label != '':
                    l2 = nlp(compare_label)
                    siml[transition1.label,
                         transition2.label] = l1.similarity(l2)

    return siml
