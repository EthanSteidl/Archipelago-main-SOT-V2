from worlds.seaofthieves.Items.Items import Items, em_flags
import typing
from ..Configurations import SotOptionsDerived
from BaseClasses import MultiWorld
import copy
from ..Items.Items import Items,ItemCollection, ItemDetail
from ..Regions.RegionDetails import Regions
from ..Regions.ConnectionDetails import ConnectionDetails
from ..Items.Items import ItemCollection,ItemReqEvalOr,ItemReqEvalAnd





def create_rules(options: SotOptionsDerived, world: MultiWorld):

    rules: typing.List[ConnectionDetails] = []

    rules.append(ConnectionDetails(Regions.R_MENU, Regions.R_PLAYER_SHIP, ItemReqEvalOr([])))
    rules.append(ConnectionDetails(Regions.R_PLAYER_SHIP, Regions.R_OPEN_SEA,
                                                         ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_OPEN_SEA_ASHEN,
                                                         ItemReqEvalOr([ItemReqEvalAnd([Items.sail_inferno])])))
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_OPEN_SEA_SHARED, ItemReqEvalOr([])))
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA_ASHEN, Regions.R_OPEN_SEA_SHARED, ItemReqEvalOr([])))
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_DOMAIN_EM,
                                                         ItemReqEvalOr([
                                                             ItemReqEvalAnd([Items.emissary_ma]),
                                                             ItemReqEvalAnd([Items.emissary_gh]),
                                                             ItemReqEvalAnd([Items.emissary_oos]),
                                                             ItemReqEvalAnd([Items.emissary_af]),
                                                             ItemReqEvalAnd([Items.emissary_rb])]
                                                         )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_AF,
                                                         ItemReqEvalOr([
                                                             ItemReqEvalAnd([
                                                                 Items.sail, Items.voyages_af, Items.emissary_af]
                                                             )]
                                                         )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_RB,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_rb, Items.emissary_rb]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_MA,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_ma, Items.emissary_ma]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_GH,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_gh, Items.emissary_gh]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_OOS,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_oos, Items.emissary_oos]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_SV,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.ship_weapons,
                                           Items.personal_weapons, Items.emissary_rb]
                                       )],
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_GF,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.ship_weapons,
                                           Items.personal_weapons, Items.emissary_af]
                                       )],
                                   )))
    # endregion

    # region Connect Ashen Sea Emissary
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA_ASHEN, Regions.R_DOMAIN_EM_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([Items.emissary_ma]),
                                       ItemReqEvalAnd([Items.emissary_gh]),
                                       ItemReqEvalAnd([Items.emissary_oos]),
                                       ItemReqEvalAnd([Items.emissary_af]),
                                       ItemReqEvalAnd([Items.emissary_rb])]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_AF_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_af, Items.emissary_af]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_RB_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_rb, Items.emissary_rb]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_MA_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_ma, Items.emissary_ma]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_GH_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_gh, Items.emissary_gh]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_OOS_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_oos, Items.emissary_oos]
                                       )]
                                   )))
    # endregion

    # region Connect Open Sea to Things Within

    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_ISLANDS,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_FORTRESSES,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))

    required_seals: typing.List[ItemDetail] = copy.deepcopy(ItemCollection.seals)
    world.random.shuffle(required_seals)
    for i in range(len(required_seals) - options.menuSettings.fodSealRequirement):
        required_seals.pop()

    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_FORT_OF_THE_DAMNED,
                                   ItemReqEvalOr([ItemReqEvalAnd(required_seals)])))
    # endregion

    # region Connect Ashen Sea to Things Within

    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_ISLANDS_ASHEN,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_FORTRESSES_ASHEN,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
    # endregion

    # region Connect Shared Sea to Things Within
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA_SHARED, Regions.R_OTHER_SHIP,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
    # endregion
    
    return rules