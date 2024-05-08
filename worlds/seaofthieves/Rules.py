import random

from worlds.seaofthieves.Items.Items import Items

from .Configurations import SotOptionsDerived
from BaseClasses import MultiWorld
import copy
from .Items.Items import ItemDetail
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
from .Regions.ConnectionDetails import ConnectionDetails
from .Regions.Regions import Regions,RegionAdder
from .Items.Items import ItemCollection,ItemReqEvalOr,ItemReqEvalAnd
from .Regions.RegionConnectionRules import create_rules

def set_rules(world: MultiWorld, options: SotOptionsDerived.SotOptionsDerived, player: int, regionAdder: RegionAdder):

    # Make Region Connection Rules
    rules = create_rules(options, world)
    for rule in rules:
        regionAdder.connectFromDetails2(world, rule)

    # Make Location Rules
    regionAdder.addRulesForLocationsInRegions(world)

    # Make Win Condition Rules
    world.completion_condition[player] = lambda state: state.has(Items.pirate_legend.name, player)
    return rules
