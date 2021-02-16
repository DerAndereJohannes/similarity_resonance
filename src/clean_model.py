from pm4py.objects.petri.petrinet import PetriNet


def clean_transitions(model: PetriNet) -> None:
    for t in model.transitions:
        if t.label and t.label.strip() == '':
            t.label = None
