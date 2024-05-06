from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.Name import Name
from ...Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items
class SettingsMenuQuestAll:

    def __init__(self, fodSealRequirement=3):
        self.fodSealRequirement = fodSealRequirement



class MenuQuestAll(LocationsBase):

    L_PIRATE_POCKET = "Item in your pocket"
    L_PIRATE_FOD = "Defeat Graymarrow"


    def __init__(self):
        super().__init__()
        self.x = [0, 0, 0, 0]

        reg = RegionNameCollection()
        reg.addFromList([Name.MENU])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], self.x[3], False), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_PIRATE_POCKET, wlc, True))

        reg = RegionNameCollection()
        reg.addFromList([Name.FORT_OF_THE_DAMNED])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.voyage_of_destiny])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], self.x[3], False), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_PIRATE_FOD, wlc, True))



