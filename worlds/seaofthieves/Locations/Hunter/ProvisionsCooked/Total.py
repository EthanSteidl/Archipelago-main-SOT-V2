from ...Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ...LocationsBase import LocationsBase
from ....Regions.RegionCollection import RegionNameCollection
from ....Regions.Name import Name
from ....Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items

class SettingsHunterTotalCooked:

    def __init__(self, cookBurnAny=1):
        self.cookBurnAny = cookBurnAny

    def getSettingForLocName(self, name: str):
        if name == HunterTotal.L_H_COOKBURNANY:
            return self.cookBurnAny

        # default for it to be enabled
        return 1
class HunterTotal(LocationsBase):

    #cat names
    L_H_COOKBURNANY = "Cook or burn anything (H)"






    def __init__(self):
        super().__init__()

        reg = RegionNameCollection()
        reg.addFromList([Name.PLAYER_SHIP])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(3, 0, 0,), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_H_COOKBURNANY, wlc, True))



