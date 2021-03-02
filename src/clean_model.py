from pm4py.objects.petri.petrinet import PetriNet


def clean_transitions(model: PetriNet) -> None:
    """Change transitions with empty string label to invisible transitions.

    Args:
        model (PetriNet): Model to clean.
    """
    for t in model.transitions:
        if t.label and t.label.strip() == '':
            t.label = None
