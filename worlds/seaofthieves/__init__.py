import os
from worlds.seaofthieves.Items.Items import *
from worlds.seaofthieves.Locations.Locations import *
from .Options import SOTOptions
from .Rules import set_rules
import base64
from worlds.seaofthieves.Regions.Regions import create_regions
from BaseClasses import Item, Tutorial, ItemClassification, LocationProgressType
from worlds.AutoWorld import World, WebWorld
from .Locations.LocationCollection import LocationDetailsCollection
from .Locations.LocationOptions import LocationOptions
from Fill import FillError, fill_restrictive
from .Regions.Regions import RegionAdder
from .Locations.Seals import Seals
from ..generic.Rules import add_rule, exclusion_rules
from .Configurations import SotOptionsDerived
from .Locations.Menu import QuestMenu
import collections
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
        self.locationCollection.applyOptions(self.sotOptionsDerived)


        return

    def fill_hook(self, progitempool, usefulitempool, filleritempool, fill_locations):
        return


    def pre_fill(self) -> None:
        self.pre_fill_seals()
        return


    def create_regions(self):
        self.regionAdder: RegionAdder = create_regions(self.multiworld, self.sotOptionsDerived, self.player, self.locationCollection)

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player, self.locationCollection, self.regionAdder)


    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        item = SOTItem(name, ItemClassification.progression, item_id, self.player)
        return item

    #def get_pre_fill_items(self):
    #    return

    def create_items(self):
        thisWorldsLocCount = self.locationCollection.getLocCount()

        items_to_add_to_pool = 0

        for detail in ItemCollection.lst:
            items_to_add_to_pool += 1
            self.multiworld.itempool.append(SOTItem(detail.name, ItemClassification.progression, detail.id, self.player))

        #sotOptions: SOTOptions = self.options
        #if sotOptions.

        #do generic multiworld exclude logic here by appending the items
        for detail in ItemCollection.seals:
            self.itemCollection.items_not_randomized.append(SOTItem(detail.name, ItemClassification.progression, detail.id, self.player))

        fillerCount = thisWorldsLocCount - items_to_add_to_pool - len(ItemCollection.seals)

        if fillerCount > 0:
            for i in range(0,fillerCount-1):
                fillItem = self.getFillerItem()
                self.multiworld.itempool.append(fillItem)


    def getFillerItem(self):
        filler_list = [Items.Filler.gold_50, Items.Filler.gold_100, Items.Filler.gold_500]
        det: ItemDetail = self.multiworld.random.choice(filler_list)
        return SOTItem(det.name, ItemClassification.filler,  det.id, self.player)


    def get_filler_item_name(self) -> str:
        return self.getFillerItem().name


    def generate_output(self, output_directory: str):
        if self.multiworld.players != 1:
            return

        maps = {}
        for i in self.multiworld.get_locations():
            locId = i.name
            if(i.item == None):
                item_name = self.get_filler_item_name()
            else:
                item_name = i.item.name
            maps[locId] = item_name

        data = {
            "slot_data": self.fill_slot_data(),
            "Location_to_item": maps,
            #"location_to_item": {self.location_name_to_id[i.name] : self.item_name_to_id[i.item.name] for i in self.multiworld.get_locations()},
        }

        options_filename = f"{self.multiworld.get_out_file_name_base(self.player)}_Options.apsmSOTOPT"
        with open(os.path.join(output_directory, options_filename), 'wb') as f:
            pickle.dump(self.sotOptionsDerived, f)

        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apsmSOT"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)


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

        seal_items = self.itemCollection.items_not_randomized
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

