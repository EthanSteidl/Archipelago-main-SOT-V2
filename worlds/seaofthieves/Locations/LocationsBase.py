

from .Locations import LocDetails, WebLocation, WebLocationCollection
class LocationsBase:


    def __init__(self):
        self.locations: typing.List[LocDetails] = []

    def getLocations(self):
        return self.locations

    def addUniques(self, name: str, wlc: WebLocationCollection):
        count = 1
        for wl in wlc:
            self.locations.append(LocDetails(name + ": " + str(count), WebLocationCollection([wl])))
            count += 1
