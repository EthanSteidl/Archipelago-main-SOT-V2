import os

import json
from worlds.seaofthieves.Items.Items import *
from .Options import SOTOptions
from .Rules import set_rules
from BaseClasses import Location
from worlds.seaofthieves.Regions.Regions import create_regions
from BaseClasses import Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Locations.LocationCollection import LocationDetailsCollection
from .Locations.LocationOptions import LocationOptions
from Fill import fill_restrictive
from .Regions.Regions import RegionAdder
from .Locations.Seals import Seals
from .Configurations import SotOptionsDerived
from .Locations.Menu import QuestMenu
import collections
from .ClientInput import ClientInput
from .Items.ItemAdder import create_items
import pickle
class SOTWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Sea of Thieves for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ethan Steidl"]
    )]


class SOTWorld(World):
    """ 
    A pirate game made by Rare
    """


    MAX_ISLANDS = 20 #number of hints
    game = "Sea of Thieves"
    topology_present = False

    web = SOTWeb()

    sotOptionsDerived: SotOptionsDerived.SotOptionsDerived

    itemCollection = ItemCollection()
    item_name_to_id = itemCollection.getDict()

    #locationOptions: LocationOptions = LocationOptions()
    locationCollection = LocationDetailsCollection()
    locationCollection.addAll()
    location_name_to_id = locationCollection.toDict()


    #location_name_to_id = {}
    data_version = 1
    options_dataclass = SOTOptions
    regionAdder: RegionAdder

    def generate_early(self) -> None:
        self.sotOptionsDerived = SotOptionsDerived.SotOptionsDerived(self.options)
        self.sotOptionsDerived.player_name = self.multiworld.player_name[self.player]
        self.locationCollection = LocationDetailsCollection()
        self.locationCollection.applyOptions(self.sotOptionsDerived)
        self.locationCollection.addAll()
        #self.location_name_to_id = {} #self.locationCollection.toDict()


        return

    def fill_hook(self, progitempool, usefulitempool, filleritempool, fill_locations):
        return


    def pre_fill(self) -> None:
        self.pre_fill_sail()
        self.pre_fill_seals()

        return


    def create_regions(self):
        self.regionAdder: RegionAdder = create_regions(self.multiworld, self.sotOptionsDerived, self.player, self.locationCollection)

    def set_rules(self):
        self.region_rules = set_rules(self.multiworld, self.sotOptionsDerived, self.player, self.regionAdder)


    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        item = SOTItem(name, ItemClassification.progression, item_id, self.player)
        return item


    def create_items(self):
        thisWorldsLocCount = self.locationCollection.getLocCount()
        create_items(self.multiworld, thisWorldsLocCount, self.sotOptionsDerived, self.itemCollection, self.player)

    def get_filler_item_name(self) -> str:
        return self.itemCollection.getFillerItemName()


    def generate_output(self, output_directory: str):

        #Utils.visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.multiworld.get_out_file_name_base(self.player)}.svg")
        if self.sotOptionsDerived.experimentals:
            self.mapss = {}
            self.locSequence = {}
            for i in self.multiworld.get_locations(self.player):
                locId = i.name
                if(i.item == None):
                    item_name = self.get_filler_item_name()
                else:
                    item_name = i.item.name
                self.mapss[locId] = item_name
                self.locSequence[i.address] = i.name

            data = {
                "slot_data": self.fill_slot_data(),
                "Location_to_item": self.mapss,
                "locSequence": self.locSequence,
                #"location_to_item": {self.location_name_to_id[i.name] : self.item_name_to_id[i.item.name] for i in self.multiworld.get_locations()},
            }

            filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apsmSOT"
            with open(os.path.join(output_directory, filename), 'w') as f:
                json.dump(data, f)

        clientInputs: ClientInput = ClientInput()
        clientInputs.sotOptionsDerived = self.sotOptionsDerived
        clientInputs.regionRules = self.region_rules
        client_file = f"{self.multiworld.get_out_file_name_base(self.player)}.apsmSOTCI"
        output_file_and_directory = os.path.join(output_directory, client_file)
        clientInputs.to_file(output_file_and_directory)




    def fill_slot_data(self):
        # The client needs to know where each seal is
        dic = {}
        hint_max = 200

        #dic["SEAL"] = self.sealHints()
        dic["HINTS_GENERAL"] = self.generalHints(hint_max)
        dic["HINTS_PERSONAL_PROG"] = self.personalProgressionHints(hint_max)
        dic["HINTS_OTHER_PROG"] = self.otherProgressionHints(hint_max)
        return dic

    def generalHints(self, max):

        cnt = 0
        hints = {}

        for sphere in self.multiworld.get_spheres():
            for sphere_location in sphere:
                if (sphere_location.player == self.player or sphere_location.item.player == self.player):

                    hints[str(cnt)] = self.create_hint(sphere_location)
                    cnt += 1
                    if(cnt >= max):
                        return hints

        return hints

    def personalProgressionHints(self, max):
        cnt = 0
        hints = {}

        for sphere in self.multiworld.get_spheres():
            for sphere_location in sphere:
                if (sphere_location.player == self.player or sphere_location.item.player == self.player) and sphere_location.item.classification == ItemClassification.progression:

                    hints[str(cnt)] = self.create_hint(sphere_location)
                    cnt += 1
                    if(cnt >= max):
                        return hints
        return hints

    def otherProgressionHints(self, max):
        cnt = 0
        hints = {}

        for sphere in self.multiworld.get_spheres():
            for sphere_location in sphere:
                if (sphere_location.player != self.player and sphere_location.item.player != self.player) and sphere_location.item.classification == ItemClassification.progression:

                    hints[str(cnt)] = self.create_hint(sphere_location)
                    cnt += 1
                    if(cnt >= max):
                        return hints
        return hints
    def sealHints(self):

        #TODO hints specific to SEALS
        return {}

    def create_hint(self, loc: Location) -> str:
        loc_name = loc.name
        item_name = loc.item.name
        for_player = loc.item.player
        sending_world = loc.player

        if(for_player == self.player):
            return '{} in world {} holds your {}'.format(loc_name, sending_world, item_name)
        return '{} holds {} for player {}'.format(loc_name, item_name, for_player)

    def pre_fill_seals(self) -> None:

        #right now we just have seals, so this works, but it wont soon

        seal_items = [
            self.create_item(Items.seal_gh.name),
            self.create_item(Items.seal_ma.name),
            self.create_item(Items.seal_af.name),
            self.create_item(Items.seal_rb.name),
            self.create_item(Items.seal_oos.name)
        ]
        seal_locations = [
            self.multiworld.get_location(Seals.Seals.L_VOYAGE_COMP_GH_TOTAL, self.player),
            self.multiworld.get_location(Seals.Seals.L_VOYAGE_COMP_MA_TOTAL, self.player),
            self.multiworld.get_location(Seals.Seals.L_VOYAGE_COMP_OOS_TOTAL, self.player),
            self.multiworld.get_location(Seals.Seals.L_VOYAGE_COMP_AF_TOTAL, self.player),
            self.multiworld.get_location(Seals.Seals.L_VOYAGE_COMP_RB_TOTAL, self.player)
        ]

        for i in seal_items:
            self.item_name_to_id[i.name] = i.code

        all_state = self.multiworld.get_all_state(use_cache=True)

        self.random.shuffle(seal_locations)

        fill_restrictive(self.multiworld, all_state, seal_locations, seal_items, True, lock=True,
                         name="SOT Seals")

        fod_location = self.multiworld.get_location(QuestMenu.MenuQuestAll.L_PIRATE_FOD, self.player)
        self.item_name_to_id[Items.pirate_legend.name] = Items.pirate_legend.id
        itm = self.create_item(Items.pirate_legend.name)
        fill_restrictive(self.multiworld, all_state, [fod_location], [itm], True, lock=True,
                         name="SOT Seals")





    def pre_fill_sail(self) -> None:

        itm = SOTItem(Items.sail.name, ItemClassification.progression, Items.sail.id, self.player)
        sail_item_list: typing.List[SOTItem] = [itm]

        locs = []
        for loc in self.multiworld.get_locations(self.player):
            locs.append(loc)

        all_state = self.multiworld.get_all_state(use_cache=True)
        self.random.shuffle(locs)

        fill_restrictive(self.multiworld, all_state, locs, sail_item_list, True, lock=True,
                         name="SOT Sail")
