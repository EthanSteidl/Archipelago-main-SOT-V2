import copy
import typing

from BaseClasses import MultiWorld, Region, Entrance
from worlds.seaofthieves.Options import SOTOptions
from .Name import Name
from worlds.seaofthieves.Locations.Locations import *
from ..Locations.LocationCollection import LocationDetailsCollection
from ...generic.Rules import add_rule, exclusion_rules
from ..Items.Items import Items
from ..Configurations import SotOptionsDerived

class SOTRegion(Region):
    subregions: typing.List[Region] = []

    def __init__(self, regionName: str, player: int, world, hint: str | None = None):
        super().__init__(regionName, player, world, hint)


class RegionAdder:



    def __init__(self, player: int, locationDetailsCollection: LocationDetailsCollection, options: SotOptionsDerived.SotOptionsDerived):
        self.player = player

        self.locationDetailsCollection = locationDetailsCollection
        self.options: SotOptionsDerived.SotOptionsDerived = options
        pass

    def addRulesForLocationsInRegions(self, world: MultiWorld):
        player = self.player

        temp = world.get_locations(self.player)
        for lll in temp:

            #for some reason, get_location needs to be called and we cant use the return of get_locations
            LOC = world.get_location(lll.name, player)
            locDetails = LOC.locDetails

            if not locDetails.doRandomize:
                exclusion_rules(world, self.player, {LOC.name})
            else:
                locDetails.setLambda(LOC, player)




    def add(self, regNameStr: str, world: MultiWorld):

        sotRegion = SOTRegion(regNameStr, self.player, world)

        locations: list[SOTLocation] = self.locationDetailsCollection.getLocationsForRegion(sotRegion.name, self.player)
        for loc in locations:
            loc.parent_region = sotRegion
        sotRegion.locations.extend(locations)
        world.regions.append(sotRegion)

    def connect(self, world: MultiWorld, source: str, target: str, rule=None) -> None:
        sourceRegion = world.get_region(source, self.player)
        targetRegion = world.get_region(target, self.player)
        sourceRegion.connect(targetRegion, rule=rule)

    def connect2(self, world: MultiWorld, source: str, target: str, rule=None) -> None:
        self.connect(world, source, target, rule)
        self.connect(world, target, source, rule)

#REG_NAME_EM_RB_VOYAGE = "Seas of Bones"

def create_regions(world: MultiWorld, options: SotOptionsDerived.SotOptionsDerived, player: int, locationDetailsCollection: LocationDetailsCollection) -> RegionAdder:

    region_adder = RegionAdder(player, locationDetailsCollection, options)
    region_adder.add(Name.MENU, world)
    region_adder.add(Name.PLAYER_SHIP, world)
    region_adder.add(Name.OTHER_SHIP, world)
    region_adder.add(Name.OPEN_SEA, world)
    region_adder.add(Name.ROAR, world)
    region_adder.add(Name.ISLANDS, world)
    region_adder.add(Name.FORTRESSES, world)
    region_adder.add(Name.FORT_OF_THE_DAMNED, world)

    region_adder.add(Name.DOMAIN_EM, world)
    region_adder.add(Name.DOMAIN_AF, world)
    region_adder.add(Name.DOMAIN_RB, world)
    region_adder.add(Name.DOMAIN_MA, world)
    region_adder.add(Name.DOMAIN_OOS, world)
    region_adder.add(Name.DOMAIN_GH, world)
    region_adder.add(Name.DOMAIN_SV, world)
    region_adder.add(Name.DOMAIN_GF, world)

    return region_adder




