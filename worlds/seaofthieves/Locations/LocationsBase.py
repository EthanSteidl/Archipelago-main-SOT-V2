

from .Locations import LocDetails, WebLocation, WebLocationCollection
import typing
class LocationsBase:


    def __init__(self):
        self.locations: typing.List[LocDetails] = []

    def getLocations(self):
        return self.locations

    def update_doRand(self, conditional: bool):
        self.doRand = conditional

    def addUniques(self, name: str, wlc: WebLocationCollection, doRand: bool):
        count = 1
        for wl in wlc:
            self.locations.append(LocDetails(name + ": " + str(count), WebLocationCollection([wl]), doRand))
            count += 1
