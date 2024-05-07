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
import typing
from worlds.seaofthieves.Regions.RegionDetails import RegionDetails
from worlds.seaofthieves.Regions.ConnectionDetails import ConnectionDetails

class Regions(list):

    R_MENU: RegionDetails = RegionDetails("Menu")
    R_PLAYER_SHIP: RegionDetails = RegionDetails("Your Ship")
    R_OTHER_SHIP: RegionDetails = RegionDetails("Another's Ship")

    R_OPEN_SEA: RegionDetails = RegionDetails("Open Sea")
    R_OPEN_SEA_ASHEN: RegionDetails = RegionDetails("Ashen Sea")
    R_OPEN_SEA_SHARED: RegionDetails = RegionDetails("The Sea")

    R_ISLANDS_ASHEN: RegionDetails = RegionDetails("Ashen Islands")
    R_ISLANDS: RegionDetails = RegionDetails("Islands")
    R_FORTRESSES: RegionDetails = RegionDetails("Fortresses")
    R_FORTRESSES_ASHEN: RegionDetails = RegionDetails("Ashen Fortresses")

    R_DOMAIN_EM: RegionDetails = RegionDetails("Seas of Emissarys")
    R_DOMAIN_AF: RegionDetails = RegionDetails("Sea of Athena")
    R_DOMAIN_RB: RegionDetails = RegionDetails("Sea of Reapers")
    R_DOMAIN_MA: RegionDetails = RegionDetails("Sea of Merchants")
    R_DOMAIN_OOS: RegionDetails = RegionDetails("Sea of Souls")
    R_DOMAIN_GH: RegionDetails = RegionDetails("Sea of Hoarders")

    R_DOMAIN_EM_ASHEN: RegionDetails = RegionDetails("Ashen Seas of Emissarys")
    R_DOMAIN_GH_ASHEN: RegionDetails = RegionDetails("Ashen Sea of Hoarders")
    R_DOMAIN_AF_ASHEN: RegionDetails = RegionDetails("Ashen Sea of Athena")
    R_DOMAIN_RB_ASHEN: RegionDetails = RegionDetails("Ashen Sea of Reapers")
    R_DOMAIN_MA_ASHEN: RegionDetails = RegionDetails("Ashen Sea of Merchants")
    R_DOMAIN_OOS_ASHEN: RegionDetails = RegionDetails("Ashen Sea of Souls")

    R_DOMAIN_SV: RegionDetails = RegionDetails("Sea of Servants")
    R_DOMAIN_GF: RegionDetails = RegionDetails("Sea of Guardians")
    R_FORT_OF_THE_DAMNED: RegionDetails = RegionDetails("Fort of the Damned")




class SOTRegion(Region):
    subregions: typing.List[Region] = []

    def __init__(self, regionName: str, player: int, world, hint: typing.Optional[str] = None):
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




    def add(self, region_details: RegionDetails, world: MultiWorld):

        sotRegion = SOTRegion(region_details.name, self.player, world)

        locations: typing.List[SOTLocation] = self.locationDetailsCollection.getLocationsForRegion(sotRegion.name, self.player)
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

    def connectFromDetails2(self, world: MultiWorld, details: ConnectionDetails):
        self.connect(world, details.start.name, details.end.name, details.lamb(self.player))
        self.connect(world, details.end.name, details.start.name, details.lamb(self.player))

#REG_NAME_EM_RB_VOYAGE = "Seas of Bones"

def create_regions(world: MultiWorld, options: SotOptionsDerived.SotOptionsDerived, player: int, locationDetailsCollection: LocationDetailsCollection) -> RegionAdder:

    region_adder = RegionAdder(player, locationDetailsCollection, options)

    for region_detail in Regions.__dict__.items():
        if region_detail[0].startswith("R_"):
            region_adder.add(region_detail[1], world)

    return region_adder




