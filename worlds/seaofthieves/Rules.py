import random

from worlds.seaofthieves.Items.Items import Items, em_flags
from worlds.seaofthieves.Regions.Regions import *

from ..generic.Rules import add_rule, exclusion_rules
from .Locations.Voyager.VoyageQuestAthena import VoyageQuestAthena
from .Locations.Voyager.VoyageQuestMa import VoyageQuestMa
from .Locations.Voyager.VoyageQuestGh import VoyageQuestGh
from .Locations.Voyager.VoyageQuestOos import VoyageQuestOos
from .Locations.Voyager.VoyageQuestRor import VoyageQuestRor
from .Locations.Rouge.RogueQuestAll import  RogueQuestAll
from .Locations.Menu.QuestMenu import MenuQuestAll
from .Locations.LocationCollection import LocationDetailsCollection
from .Regions.Name import Name
from .Locations.Hunter.ProvisionsCooked import BurntAboard, CookedAboard, Total




def set_rules(world: MultiWorld, options: SOTOptions, player: int, locCollection: LocationDetailsCollection, regionAdder: RegionAdder):

    regionAdder.connect2(world, Name.MENU, Name.PLAYER_SHIP)

    regionAdder.connect2(world, Name.PLAYER_SHIP, Name.OPEN_SEA,
                         lambda state: state.has(Items.sail.name, player))

    regionAdder.connect2(world, Name.OPEN_SEA, Name.DOMAIN_EM,
                         lambda state: state.has_any([
                             Items.emissary_ma.name,
                             Items.emissary_gh.name,
                             Items.emissary_oos.name,
                             Items.emissary_af.name,
                             Items.emissary_rb.name
                         ], player))

    required_seal_names = [Items.seal_gh.name,
                           Items.seal_ma.name,
                           Items.seal_oos.name,
                           Items.seal_af.name,
                           Items.seal_rb.name]

    world.random.shuffle(required_seal_names)
    selected_seal_names = []
    for i in range(options.sealCount):
        selected_seal_names.append(required_seal_names[i])

    regionAdder.connect2(world, Name.OPEN_SEA, Name.FORT_OF_THE_DAMNED,
                        lambda state: state.has_all(selected_seal_names.copy(), player))

    regionAdder.connect2(world, Name.OPEN_SEA, Name.ISLANDS)
    regionAdder.connect2(world, Name.OPEN_SEA, Name.FORTRESSES)
    regionAdder.connect2(world, Name.OPEN_SEA, Name.OTHER_SHIP)
    regionAdder.connect2(world, Name.OPEN_SEA, Name.ROAR,
                         lambda state: state.has(Items.sail_inferno.name, player))

    #ultimately, it is not fun gameplay for players to do voyages without being able to sell/emy up, so just give both
    regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_AF,
                         lambda state: state.has_all([Items.emissary_af.name, Items.voyages_af.name], player))
    regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_RB,
                         lambda state: state.has_all([Items.emissary_rb.name, Items.voyages_rb.name], player))
    regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_MA,
                         lambda state: state.has_all([Items.emissary_ma.name, Items.voyages_ma.name], player))
    regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_OOS,
                         lambda state: state.has_all([Items.emissary_oos.name, Items.voyages_oos.name], player))
    regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_GH,
                         lambda state: state.has_all([Items.emissary_gh.name, Items.voyages_gh.name], player))
    regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_SV,
                         lambda state: state.has(Items.emissary_rb.name, player))
    regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_GF,
                         lambda state: state.has(Items.emissary_af.name, player))

    locCollection.applyOptions(options)
    regionAdder.addRulesForLocationsInRegions(world)

    #world.completion_condition[player] = lambda state: state.can_reach(MenuQuestAll.L_PIRATE_FOD, "Location", player)
    world.completion_condition[player] = lambda state: state.has(Items.pirate_legend.name, player)


