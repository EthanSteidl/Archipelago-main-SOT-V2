import random

from worlds.seaofthieves.Items.Items import Items, em_flags

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

#
# def set_rules(world: MultiWorld, options: SOTOptions, player: int, locCollection: LocationDetailsCollection, regionAdder: RegionAdder):
#
#     regionAdder.connect2(world, Name.MENU, Name.PLAYER_SHIP)
#
#     regionAdder.connect2(world, Name.PLAYER_SHIP, Name.OPEN_SEA,
#                          lambda state: state.has(Items.sail.name, player))
#
#     regionAdder.connect2(world, Name.OPEN_SEA, Name.DOMAIN_EM,
#                          lambda state: state.has_any([
#                              Items.emissary_ma.name,
#                              Items.emissary_gh.name,
#                              Items.emissary_oos.name,
#                              Items.emissary_af.name,
#                              Items.emissary_rb.name
#                          ], player))
#
#     required_seal_names = [Items.seal_gh.name,
#                            Items.seal_ma.name,
#                            Items.seal_oos.name,
#                            Items.seal_af.name,
#                            Items.seal_rb.name]
#
#     world.random.shuffle(required_seal_names)
#     selected_seal_names = []
#     for i in range(options.sealCount):
#         selected_seal_names.append(required_seal_names[i])
#
#     regionAdder.connect2(world, Name.OPEN_SEA, Name.FORT_OF_THE_DAMNED,
#                         lambda state: state.has_all(selected_seal_names.copy(), player))
#
#     regionAdder.connect2(world, Name.OPEN_SEA, Name.ISLANDS)
#     regionAdder.connect2(world, Name.OPEN_SEA, Name.FORTRESSES)
#     regionAdder.connect2(world, Name.OPEN_SEA, Name.OTHER_SHIP)
#     regionAdder.connect2(world, Name.OPEN_SEA, Name.ROAR,
#                          lambda state: state.has(Items.sail_inferno.name, player))
#
#     #ultimately, it is not fun gameplay for players to do voyages without being able to sell/emy up, so just give both
#     regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_AF,
#                          lambda state: state.has_all([Items.emissary_af.name, Items.voyages_af.name], player))
#     regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_RB,
#                          lambda state: state.has_all([Items.emissary_rb.name, Items.voyages_rb.name], player))
#     regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_MA,
#                          lambda state: state.has_all([Items.emissary_ma.name, Items.voyages_ma.name], player))
#     regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_OOS,
#                          lambda state: state.has_all([Items.emissary_oos.name, Items.voyages_oos.name], player))
#     regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_GH,
#                          lambda state: state.has_all([Items.emissary_gh.name, Items.voyages_gh.name], player))
#     regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_SV,
#                          lambda state: state.has(Items.emissary_rb.name, player))
#     regionAdder.connect2(world, Name.DOMAIN_EM, Name.DOMAIN_GF,
#                          lambda state: state.has(Items.emissary_af.name, player))
#
#     regionAdder.addRulesForLocationsInRegions(world)
#
#     world.completion_condition[player] = lambda state: state.has(Items.pirate_legend.name, player)


############################
# #just in case you need a backup
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_MENU, Regions.R_PLAYER_SHIP, ItemReqEvalOr([])))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_PLAYER_SHIP, Regions.R_OPEN_SEA,
#                                                              ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_OPEN_SEA_ASHEN,
#                                                              ItemReqEvalOr([ItemReqEvalAnd([Items.sail_inferno])])))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_OPEN_SEA_SHARED, ItemReqEvalOr([])))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA_ASHEN, Regions.R_OPEN_SEA_SHARED, ItemReqEvalOr([])))
#     # endregion
#
#     #region Connect Open Sea Emissary
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_DOMAIN_EM,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([Items.emissary_ma]),
#                                                                  ItemReqEvalAnd([Items.emissary_gh]),
#                                                                  ItemReqEvalAnd([Items.emissary_oos]),
#                                                                  ItemReqEvalAnd([Items.emissary_af]),
#                                                                  ItemReqEvalAnd([Items.emissary_rb])]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_AF,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.voyages_af, Items.emissary_af]
#                                                                  )]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_RB,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.voyages_rb, Items.emissary_rb]
#                                                                  )]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_MA,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.voyages_ma, Items.emissary_ma]
#                                                                  )]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_GH,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.voyages_gh, Items.emissary_gh]
#                                                                  )]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_OOS,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.voyages_oos, Items.emissary_oos]
#                                                                  )]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_SV,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.ship_weapons,
#                                                                      Items.personal_weapons, Items.emissary_rb]
#                                                                  )],
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_GF,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.ship_weapons,
#                                                                      Items.personal_weapons, Items.emissary_af]
#                                                                  )],
#                                                              )))
#     #endregion
#
#     #region Connect Ashen Sea Emissary
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA_ASHEN, Regions.R_DOMAIN_EM_ASHEN,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([Items.emissary_ma]),
#                                                                  ItemReqEvalAnd([Items.emissary_gh]),
#                                                                  ItemReqEvalAnd([Items.emissary_oos]),
#                                                                  ItemReqEvalAnd([Items.emissary_af]),
#                                                                  ItemReqEvalAnd([Items.emissary_rb])]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_AF_ASHEN,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.voyages_af, Items.emissary_af]
#                                                                  )]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_RB_ASHEN,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.voyages_rb, Items.emissary_rb]
#                                                                  )]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_MA_ASHEN,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.voyages_ma, Items.emissary_ma]
#                                                                  )]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_GH_ASHEN,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.voyages_gh, Items.emissary_gh]
#                                                                  )]
#                                                              )))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_OOS_ASHEN,
#                                                              ItemReqEvalOr([
#                                                                  ItemReqEvalAnd([
#                                                                      Items.sail, Items.voyages_oos, Items.emissary_oos]
#                                                                  )]
#                                                              )))
#     #endregion
#
#     #region Connect Open Sea to Things Within
#
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_ISLANDS,
#                                                              ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_FORTRESSES,
#                                                              ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
#
#     required_seals: typing.List[ItemDetail] = copy.deepcopy(ItemCollection.seals)
#     world.random.shuffle(required_seals)
#     for i in range(len(required_seals) - options.menuSettings.fodSealRequirement):
#         required_seals.pop()
#
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_FORT_OF_THE_DAMNED,
#                                                              ItemReqEvalOr([ItemReqEvalAnd(required_seals)])))
#     #endregion
#
#     #region Connect Ashen Sea to Things Within
#
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_ISLANDS_ASHEN,
#                                                              ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_FORTRESSES_ASHEN,
#                                                              ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
#     #endregion
#
#     #region Connect Shared Sea to Things Within
#     regionAdder.connectFromDetails2(world, ConnectionDetails(Regions.R_OPEN_SEA_SHARED, Regions.R_OTHER_SHIP,
#                                                              ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))