class KnnNode:
    def __init__(self, activity):
        self.activity = activity
        self.pre_set = []
        self.post_set = []

    def set_preset(self, activity_list: list) -> None:
        self.pre_set = activity_list

    def set_postset(self, activity_list: list) -> None:
        self.post_set = activity_list

    def __repr__(self):
        return f'activity: {self.activity}, '\
            f'preset: {self.pre_set}, postset:{self.post_set}'
