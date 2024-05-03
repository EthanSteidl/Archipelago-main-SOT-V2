from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.Name import Name
from ...Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items
class SettingsVoyageQuestAthena:

    def __init__(self, completeAny=1, vale=1, ashenAthena=1, haunted=1, lyingMap=1, pictoralMap=1, shipwreckGraveyard=1, closeupMap=1, ghostGarrison=1, legendarySearchCursed=1, skullDestiny=1):
        self.completeAny = completeAny
        self.vale = vale
        self.ashenAthena = ashenAthena
        self.haunted = haunted
        self.lyingMap = lyingMap
        self.pictoralMap = pictoralMap
        self.shipwreckGraveyard = shipwreckGraveyard
        self.closeupMap = closeupMap
        self.ghostGarrison = ghostGarrison
        self.legendarySearchCursed = legendarySearchCursed
        self.skullDestiny = skullDestiny


class VoyageQuestAthena(LocationsBase):

    L_VOYAGE_COMP_AF_VALE = "Complete Legend of the Vale Voyage (AF)"
    L_VOYAGE_COMP_AF_AATHENA = "Complete Ashen Athena Voyage (AF)"
    L_VOYAGE_COMP_AF_HAUNTED = "Complete Haunted Island Voyage (AF)"
    L_VOYAGE_COMP_AF_LYING = "Complete Lying Map Voyage (AF)"
    L_VOYAGE_COMP_AF_PICTORAL = "Complete Pictoral Map Voyage (AF)"
    L_VOYAGE_COMP_AF_SHIP = "Complete Shipwreck Graveyard Voyage (AF)"
    L_VOYAGE_COMP_AF_CLOSE = "Complete Close-Up Map Voyage (AF)"
    L_VOYAGE_COMP_AF_GHOSTGAR = "Complete Ghost Garrison Voyage (AF)"
    L_VOYAGE_COMP_AF_CURSED = "Complete Search for Cursed Treasure Voyage (AF)"
    L_VOYAGE_COMP_AF_DESTINY = "Complete Skull of Destiny Voyage (AF)"

    def __init__(self):
        super().__init__()
        self.x = [1, 4, 1]


        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_VALE, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_AATHENA, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_af, Items.ship_weapons])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_HAUNTED, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_LYING, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_PICTORAL, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_SHIP, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 6), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_CLOSE, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 7), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_GHOSTGAR, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 8), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_CURSED, wlc))


        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 9), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_DESTINY, wlc))

