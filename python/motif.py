import jsonpickle
import json

class Motif:
    def __init__(self, motif, cover, coverage, pos_c, neg_c, quality, length, items, area):
        self.motif = motif
        self.cover = cover
        self.coverage = coverage
        self.pos_cov = pos_c
        self.neg_cov = neg_c
        self.obj_quality = quality
        self.length = length
        self.items = items
        self.area = area

    def toDict(self):
        return self.__dict__

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

