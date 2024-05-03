from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.Name import Name
from ...Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items
class SettingsVoyageQuestOos:

    def __init__(self, player=1, completeAny=1, bounty=1, ashenBounty=1, ghostShip=1):
        self.player = player
        self.completeAny = completeAny
        self.bounty = bounty
        self.ashenBounty = ashenBounty
        self.ghostShip = ghostShip


class VoyageQuestOos(LocationsBase):

    locations = []

    L_VOYAGE_COMP_OOS_BOUNTY = "Complete Bounty Voyage (OOS)"
    L_VOYAGE_COMP_OOS_ABOUNTY = "Complete Ashen Bounty Voyage (OOS)"
    L_VOYAGE_COMP_OOS_GHOSTSHIP = "Complete Ghost Ship Voyage (OOS)"

    def __init__(self):
        super().__init__()
        self.x = [1, 3, 1]


        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.voyages_oos, Items.sail, Items.ship_weapons, Items.personal_weapons])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_OOS_BOUNTY, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.ROAR])
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.voyages_oos, Items.sail, Items.ship_weapons, Items.personal_weapons, Items.sail_inferno])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_OOS_ABOUNTY, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.voyages_oos, Items.sail, Items.ship_weapons])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_OOS_GHOSTSHIP, wlc))
