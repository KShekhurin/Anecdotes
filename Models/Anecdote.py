import json


class Anecdote:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, id=None, text="", rating=0, in_queue=False):
        self.id = id
        self.text = text
        self.rating = rating
        self.in_queue = in_queue

    @staticmethod
    def build_from_tuple(tuple):
        if tuple is None:
            return None
        return Anecdote(tuple[0], tuple[1], tuple[2], tuple[3])