class KrgNode:
    """K-Resonance Graph node representation. Activity set = Node,
    pre/postset = outgoing arcs.
    """
    def __init__(self, activity):
        self.activity_set = activity
        self.pre_set = {}
        self.post_set = {}

    def set_preset(self, activity_list: dict) -> None:
        self.pre_set = activity_list

    def set_postset(self, activity_list: dict) -> None:
        self.post_set = activity_list

    def generate_postset(self, knn_src, knn_target, lmax, l_thresh) -> None:
        new_postset = {}
        for item1 in knn_src.post_set:
            for item2 in knn_target.post_set:
                if lmax[item1, item2] >= l_thresh:
                    new_postset[item1, item2] = 5
                elif self.all_under_l_thresh(item1, item2, lmax, l_thresh):
                    new_postset[item1, item2] = 5
                else:
                    new_postset[item1, item2] = 1

        self.post_set = new_postset

    def generate_preset(self, knn_src, knn_target, lmax, l_thresh) -> None:
        new_preset = {}
        for item1 in knn_src.pre_set:
            for item2 in knn_target.pre_set:
                if lmax[item1, item2] >= l_thresh:
                    new_preset[item1, item2] = 5
                elif self.all_under_l_thresh(item1, item2, lmax, l_thresh):
                    new_preset[item1, item2] = 5
                else:
                    new_preset[item1, item2] = 1

        self.pre_set = new_preset

    def all_under_l_thresh(self, item1, item2, lmax, l_thresh) -> bool:
        for key, value in lmax.items():
            if (item1, item2) != key:
                if item1 == key[0]:
                    if value >= l_thresh:
                        return False
                elif item2 == key[1]:
                    if value >= l_thresh:
                        return False

        return True

    def compute_edge_weights(self) -> None:
        denominator = sum(self.pre_set.values()) + sum(self.post_set.values())

        for key, value in self.pre_set.items():
            self.pre_set[key] = value / denominator

        for key, value in self.post_set.items():
            self.post_set[key] = value / denominator

    def contains(self, match) -> bool:
        return match in self.post_set.keys() or match in self.pre_set.keys()

    def __repr__(self):
        return f'Node: {self.activity_set}, '\
            f'\nOutward Arcs: {self.pre_set}{self.post_set}'
