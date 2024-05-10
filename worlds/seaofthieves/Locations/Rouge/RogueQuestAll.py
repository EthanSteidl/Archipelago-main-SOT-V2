from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items
from ..ScreenData import ScreenData

class SettingsRogueQuestAll:

    def __init__(self, seaShanty=1, grog=1, sleeping=1, sitting=1):
        self.seaShanty = seaShanty
        self.grog = grog
        self.sleeping = sleeping
        self.sitting = sitting



class RogueQuestAll(LocationsBase):

    L_ROGUE_SHANTY = "Play music for 1 minute (ROUGE)"
    L_ROUGE_GROG = "Drink 1 grog (ROUGE)"
    L_ROUGE_SLEEP = "Sleep for 1 minute (ROUGE)"
    L_ROUGE_SIT = "Sit for 1 minute (ROUGE)"


    def __init__(self, settings: SettingsRogueQuestAll):
        super().__init__()
        self.x = [5, 0, 0]
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_PLAYER_SHIP])
        lgc = ItemReqEvalOr([])


        web = WebItemJsonIdentifier(self.x[0], 0, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc, ScreenData(["Becalmed"]))])
        self.locations.append(LocDetails(self.L_ROGUE_SHANTY, wlc, settings.seaShanty > 0))

        web = WebItemJsonIdentifier(self.x[0], 1, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc, ScreenData(["Refill"]))])
        self.locations.append(LocDetails(self.L_ROUGE_GROG, wlc, settings.grog > 0))

        web = WebItemJsonIdentifier(self.x[0], 2, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc, ScreenData(["Sleep", "Wake"]))])
        self.locations.append(LocDetails(self.L_ROUGE_SLEEP, wlc, settings.sleeping > 0))

        web = WebItemJsonIdentifier(self.x[0], 3, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc, ScreenData(["Seat"]))])
        self.locations.append(LocDetails(self.L_ROUGE_SIT, wlc, settings.sitting > 0))

        web = WebItemJsonIdentifier(0, 0, 0, 0, False)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc, ScreenData(["Bell"]), True)])
        self.locations.append(LocDetails("Ring Bell", wlc, True))
