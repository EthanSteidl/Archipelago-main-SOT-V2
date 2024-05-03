from .Name import Name


class RegionNameCollection:

    def __int__(self):
        self.regions = {}

    def add(self, name: Name):
        self.regions = {}
        self.regions[name] = True

    def addFromList(self, names: list[Name]):
        self.regions = {}
        for i in range(len(names)):
            self.regions[names[i]] = True

    def contains(self, name: Name):
        return name in self.regions

    def getAllRegionStrings(self) -> list[str]:
        ret: list[str] = []
        for key in self.regions.keys():
            ret.append(key)
        return ret

    def getFirst(self) -> Name:

        #TODO this may be a problem cause if the sphere fills and is needed, then its unbeatable
        for k in self.regions.keys():
            return k
