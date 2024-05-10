from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items
from ...Locations.LocationSettingOption import LocationSettingOption
from ...Locations.ScreenData import ScreenData

class SettingsCannonsFired:
    class Balls(LocationSettingOption):
        pass
    class CursedBalls(LocationSettingOption):
        pass
    class PhantomBalls(LocationSettingOption):
        pass
    def __init__(self, defaultBalls=Balls.DEFAULT, cursedBalls=CursedBalls.DEFAULT, phantomBalls=PhantomBalls.DEFAULT):
        self.defaultBalls = defaultBalls
        self.cursedBalls = cursedBalls
        self.phantomBalls = phantomBalls



class CannonsFired(LocationsBase):

    L_ILL_CANN_DEFAULT = "Fire any Cannonball from ship"
    L_ILL_CANN_CURSED = "Fire any Cursed Cannonball from ship"
    L_ILL_CANN_PHANT = "Fire any Phantom Cannonball from ship"

    L_ILL_CANN_ANC = "Fire Anchorball from ship"
    L_ILL_CANN_BALLAST = "Fire Ballastball from ship"
    L_ILL_CANN_BARRELBALL = "Fire Barrelball from ship"
    L_ILL_CANN_BLUNDERBOMB = "Fire Blunderbomb from ship"
    L_ILL_CANN_CANNONBALL = "Fire Cannonball from ship"
    L_ILL_CANN_CHAINSHOT = "Fire Chainshot from ship"
    L_ILL_CANN_FIREBOMB = "Fire Firebomb from ship"
    L_ILL_CANN_FPCANNONBALL = "Fire Flame Phantom Cannonball from ship"
    L_ILL_CANN_GROGBALL = "Fire Grogball from ship"
    L_ILL_CANN_HELMBALL = "Fire Helmball from ship"
    L_ILL_CANN_JIGBALL = "Fire Jigball from ship"
    L_ILL_CANN_LIMPBALL = "Fire Limpball from ship"
    L_ILL_CANN_PEACEBALL = "Fire Peaceball from ship"
    L_ILL_CANN_PET = "Fire Pets from ship"
    L_ILL_CANN_PCANNONBALL = "Fire Phantom Cannonball from ship"
    L_ILL_CANN_PLAYER = "Fire Players from ship"
    L_ILL_CANN_RIGGINGBALL = "Fire Riggingball from ship"
    L_ILL_CANN_VENOMBALL = "Fire Venomball from ship"
    L_ILL_CANN_WEARYBALL = "Fire Wearyball from ship"
    L_ILL_CANN_WRAITHCANNONBALL = "Fire Wraith Cannonball from ship"


    def __init__(self, settings: SettingsCannonsFired):
        super().__init__()
        self.x = [4, 0, 1]
        self.settings = settings


        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_CANNONS])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3), reg, lgc, ScreenData(["Unload Blunderbomb"]), False, "Fire Blunderbomb"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4), reg, lgc, ScreenData(["Unload Bone Caller"]), False, "Fire Bone Caller"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5), reg, lgc, ScreenData(["Unload Cannonball"]), False, "Fire Cannonball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 6), reg, lgc, ScreenData(["Unload Chainshot"]), False, "Fire Chainshot"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 7), reg, lgc, ScreenData(["Unload Firebomb"]), False, "Fire Firebomb"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 18), reg, lgc, ScreenData(["Unload Scattershot"]), False, "Fire Scattershot")
        ])

        do_rand: bool = self.settings.defaultBalls is SettingsCannonsFired.Balls.ON
        self.locations.append(LocDetails(self.L_ILL_CANN_DEFAULT, wlc, do_rand))

        do_rand: bool = self.settings.defaultBalls is SettingsCannonsFired.Balls.UNIQUE
        self.addUniques(self.L_ILL_CANN_DEFAULT, wlc, do_rand)





        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_CANNONS])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 8), reg, lgc, ScreenData(["Unload Flame"]), False, "Fire Flame Phantom Cannonball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 15), reg, lgc, ScreenData(["Unload Phant"]), False, "Fire Phantom Cannonball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 21), reg, lgc, ScreenData(["Unload Wraith"]), False, "Fire Wraith Cannonball")
        ])


        do_rand: bool = self.settings.phantomBalls is SettingsCannonsFired.PhantomBalls.ON
        self.locations.append(LocDetails(self.L_ILL_CANN_PHANT, wlc, do_rand))

        do_rand: bool = self.settings.phantomBalls is SettingsCannonsFired.PhantomBalls.UNIQUE
        self.addUniques(self.L_ILL_CANN_PHANT, wlc, do_rand)


        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_CANNONS])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc, ScreenData(["Unload Anch"]), False, "Fire Anchorball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc, ScreenData(["Unload Ball"]), False, "Fire Ballastball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc, ScreenData(["Unload Barr"]), False, "Fire Barrelball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 9), reg, lgc, ScreenData(["Unload Grog"]), False, "Fire Grogball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 10), reg, lgc, ScreenData(["Unload Helm"]), False, "Fire Helmball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 11), reg, lgc, ScreenData(["Unload Jig"]), False, "Fire Jigball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 12), reg, lgc, ScreenData(["Unload Limp"]), False, "Fire Limpball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 13), reg, lgc, ScreenData(["Unload Peace"]), False, "Fire Peaceball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 17), reg, lgc, ScreenData(["Unload Rig"]), False, "Fire Riggingball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 19), reg, lgc, ScreenData(["Unload Ven"]), False, "Fire Venomball"),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 19), reg, lgc, ScreenData(["Unload Wea"]), False, "Fire Wearyball"),
        ])

        do_rand: bool = self.settings.cursedBalls is SettingsCannonsFired.CursedBalls.ON
        self.locations.append(LocDetails(self.L_ILL_CANN_CURSED, wlc, do_rand))

        do_rand: bool = self.settings.cursedBalls is SettingsCannonsFired.CursedBalls.UNIQUE
        self.addUniques(self.L_ILL_CANN_CURSED, wlc, do_rand)

