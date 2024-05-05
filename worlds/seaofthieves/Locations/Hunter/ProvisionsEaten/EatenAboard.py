from ...Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ...LocationsBase import LocationsBase
from ....Regions.RegionCollection import RegionNameCollection
from ....Regions.Name import Name
from ....Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items
from ....Locations.LocationSettingOption import LocationSettingOption

class SettingsHunterEatenAboard:

    class Any(LocationSettingOption):
        pass

    class Fish(LocationSettingOption):
        CATEGORICAL_NAME = 4

    class LandMeat(LocationSettingOption):
        pass

    class BigFish(LocationSettingOption):
        pass

    class Fruit(LocationSettingOption):
        pass

    class Bug(LocationSettingOption):
        pass

    def __init__(self, completeAny=Any.DEFAULT, fishCategory=Fish.DEFAULT, landMeatCategory=LandMeat.DEFAULT, bigFishCategory=BigFish.DEFAULT, fruitCategory=Fruit.DEFAULT, bugCategory=Bug.DEFAULT):
        self.any = completeAny
        self.fish = fishCategory
        self.landMeat = landMeatCategory
        self.bigFish = bigFishCategory
        self.fruit = fruitCategory
        self.bug = bugCategory

    def getSettingForLocName(self, name: str):
        if name == HunterEatenAboard.L_H_EAT:
            return self.any

        if (name == HunterEatenAboard.L_H_CAT_EAT_SPLASHTAIL or
                name == HunterEatenAboard.L_H_CAT_EAT_PONDIE or
                name == HunterEatenAboard.L_H_CAT_EAT_ISLEHOPPER or
                name == HunterEatenAboard.L_H_CAT_EAT_ANCIENTSCALE or
                name == HunterEatenAboard.L_H_CAT_EAT_PLENTIFIN or
                name == HunterEatenAboard.L_H_CAT_EAT_WILDSPLASH or
                name == HunterEatenAboard.L_H_CAT_EAT_DEVILFISH or
                name == HunterEatenAboard.L_H_CAT_EAT_BATTLEGILL or
                name == HunterEatenAboard.L_H_CAT_EAT_WRECKER or
                name == HunterEatenAboard.L_H_CAT_EAT_STORMFISH):
            return self.fish

        if name == HunterEatenAboard.L_H_CAT_EAT_LAND:
            return self.landMeat

        if name == HunterEatenAboard.L_H_CAT_EAT_BIG:
            return self.bigFish

        if name == HunterEatenAboard.L_H_CAT_EAT_BUG:
            return self.bug

        if name == HunterEatenAboard.L_H_CAT_EAT_FRUIT:
            return self.fruit

        # default for it to be enabled
        return 1
class HunterEatenAboard(LocationsBase):

    L_H_EAT = "Eat Anything (H)"

    #cat names
    L_H_CAT_EAT_SPLASHTAIL = "Eat Splashtail (H)"
    L_H_CAT_EAT_PONDIE = "Eat Pondie (H)"
    L_H_CAT_EAT_ISLEHOPPER = "Eat Islehopper (H)"
    L_H_CAT_EAT_ANCIENTSCALE = "Eat Ancientscale (H)"
    L_H_CAT_EAT_PLENTIFIN = "Eat Plentifin (H)"
    L_H_CAT_EAT_WILDSPLASH = "Eat Wildsplash (H)"
    L_H_CAT_EAT_DEVILFISH = "Eat Devilfish (H)"
    L_H_CAT_EAT_BATTLEGILL = "Eat Battlegill (H)"
    L_H_CAT_EAT_WRECKER = "Eat Wrecker (H)"
    L_H_CAT_EAT_STORMFISH = "Eat Stormfish (H)"
    L_H_CAT_EAT_LAND = "Eat Land Creature (H)"
    L_H_CAT_EAT_BIG = "Eat Shark, Megalodon, or Kraken (H)"
    L_H_CAT_EAT_BUG = "Eat Bugs (H)"
    L_H_CAT_EAT_FRUIT = "Eat Fruit (H)"






    def __init__(self, settings: SettingsHunterEatenAboard):
        super().__init__()
        self.x = [3, 1, 1]
        self.settings = settings
        self.settings.landMeat = SettingsHunterEatenAboard.LandMeat.UNIQUE
        self.settings.bug = SettingsHunterEatenAboard.Bug.UNIQUE
        self.settings.fish = SettingsHunterEatenAboard.Fish.UNIQUE
        self.settings.fruit = SettingsHunterEatenAboard.Fruit.UNIQUE

        if self.settings.any is not SettingsHunterEatenAboard.Any.OFF:
           self.add_any_sets()

        if self.settings.fish is not SettingsHunterEatenAboard.Fish.OFF:
            self.add_fish_sets()

        if self.settings.landMeat is not SettingsHunterEatenAboard.LandMeat.OFF:
            self.add_meat_set_land()

        if self.settings.bigFish is not SettingsHunterEatenAboard.BigFish.OFF:
            self.add_fish_set_big()

        if self.settings.fruit is not SettingsHunterEatenAboard.Fruit.OFF:
            self.add_fruit_set()

        if self.settings.bug is not SettingsHunterEatenAboard.Bug.OFF:
            self.add_bug_set()

    def add_any_sets(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.MENU])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2]), reg, lgc), #this is weird and also at 3,1,0
        ])
        self.locations.append(LocDetails(self.L_H_EAT, wlc))

    def add_fish_sets(self):
        self.add_fish_set_pondie()
        self.add_fish_set_splashtail()
        self.add_fish_set_islehopper()
        self.add_fish_set_ancientscale()
        self.add_fish_set_plentifin()
        self.add_fish_set_wildsplash()
        self.add_fish_set_devilfish()
        self.add_fish_set_battlegill()

    def add_land_sets(self):
        self.add_meat_set_land()

    def addFishSetLoc(self, name: str, wlc: WebLocationCollection):
        if self.settings.fish == SettingsHunterEatenAboard.Fish.OFF:
            return
        elif self.settings.fish == SettingsHunterEatenAboard.Fish.ON:
            #TODO not implemented
            return
        elif self.settings.fish == SettingsHunterEatenAboard.Fish.CATEGORICAL_NAME:
            self.locations.append(LocDetails(name, wlc))
        elif self.settings.fish == SettingsHunterEatenAboard.Fish.UNIQUE:
            self.addUniques(name, wlc)

    def addLandMeatSetLoc(self, name: str, wlc: WebLocationCollection):
        if self.settings.landMeat == SettingsHunterEatenAboard.LandMeat.OFF:
            return
        elif self.settings.landMeat == SettingsHunterEatenAboard.LandMeat.ON:
            self.locations.append(LocDetails(name, wlc))
        elif self.settings.landMeat == SettingsHunterEatenAboard.LandMeat.UNIQUE:
            self.addUniques(name, wlc)

    def addBigFishLoc(self, name: str, wlc: WebLocationCollection):
        if self.settings.bigFish == SettingsHunterEatenAboard.BigFish.OFF:
            return
        elif self.settings.bigFish == SettingsHunterEatenAboard.BigFish.ON:
            self.locations.append(LocDetails(name, wlc))
        elif self.settings.bigFish == SettingsHunterEatenAboard.BigFish.UNIQUE:
            self.addUniques(name, wlc)

    def addBugSetLoc(self, name: str, wlc: WebLocationCollection):
        if self.settings.bug == SettingsHunterEatenAboard.Bug.OFF:
            return
        elif self.settings.bug == SettingsHunterEatenAboard.Bug.ON:
            self.locations.append(LocDetails(name, wlc))
        elif self.settings.bug == SettingsHunterEatenAboard.Bug.UNIQUE:
            self.addUniques(name, wlc)

    def addFruitSetLoc(self, name: str, wlc: WebLocationCollection):
        if self.settings.fruit == SettingsHunterEatenAboard.Fruit.OFF:
            return
        elif self.settings.fruit == SettingsHunterEatenAboard.Fruit.ON:
            self.locations.append(LocDetails(name, wlc))
        elif self.settings.fruit == SettingsHunterEatenAboard.Fruit.UNIQUE:
            self.addUniques(name, wlc)
    def add_fish_set_pondie(self):

        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 6), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 7), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 8), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 9), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 10), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 11), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_EAT_PONDIE, wlc)

    def add_fish_set_splashtail(self) -> None:
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5), reg, lgc)
        ])
        self.addFishSetLoc(self.L_H_CAT_EAT_SPLASHTAIL, wlc)


    def add_fish_set_islehopper(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 12), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 13), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 14), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 15), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 16), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 17), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_EAT_ISLEHOPPER, wlc)


    def add_fish_set_ancientscale(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 19), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 20), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 21), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 22), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 23), reg, lgc)
        ])
        self.addFishSetLoc(self.L_H_CAT_EAT_ANCIENTSCALE, wlc)


    def add_fish_set_plentifin(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 24), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 25), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 26), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 27), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 28), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 29), reg, lgc)
        ])
        self.addFishSetLoc(self.L_H_CAT_EAT_PLENTIFIN, wlc)


    def add_fish_set_wildsplash(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 30), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 31), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 32), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 33), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 34), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 35), reg, lgc)
        ])
        self.addFishSetLoc(self.L_H_CAT_EAT_WILDSPLASH, wlc)

    def add_fish_set_devilfish(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 36), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 37), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 38), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 39), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 40), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 41), reg, lgc)
        ])
        self.addFishSetLoc(self.L_H_CAT_EAT_DEVILFISH, wlc)

    def add_fish_set_battlegill(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 42), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 43), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 44), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 45), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 46), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 47), reg, lgc)
        ])
        self.addFishSetLoc(self.L_H_CAT_EAT_BATTLEGILL, wlc)


    def add_fish_set_wrecker(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 48), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 49), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 50), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 51), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 52), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 53), reg, lgc)
        ])
        self.addFishSetLoc(self.L_H_CAT_EAT_WRECKER, wlc)


    def add_fish_set_stormfish(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 54), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 55), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 56), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 57), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 58), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 59), reg, lgc)
        ])
        self.addFishSetLoc(self.L_H_CAT_EAT_STORMFISH, wlc)


    def add_meat_set_land(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([
            ItemReqEvalAnd([Items.sail, Items.personal_weapons]),
            ItemReqEvalAnd([Items.sail, Items.ship_weapons])
            ])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 60), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 61), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 62), reg, lgc)
        ])
        self.addLandMeatSetLoc(self.L_H_CAT_EAT_LAND, wlc)


    def add_fish_set_big(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([
            ItemReqEvalAnd([Items.sail, Items.ship_weapons, Items.personal_weapons])
            ])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 63), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 64), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 65), reg, lgc)
        ])
        self.addBigFishLoc(self.L_H_CAT_EAT_BIG, wlc)


    def add_fruit_set(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([
            ItemReqEvalAnd([Items.sail])
            ])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 66), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 67), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 68), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 69), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 70), reg, lgc)
        ])
        self.addFruitSetLoc(self.L_H_CAT_EAT_FRUIT, wlc)



    def add_bug_set(self):
        reg = RegionNameCollection()
        reg.addFromList([Name.OPEN_SEA])
        lgc = ItemReqEvalOr([
            ItemReqEvalAnd([Items.sail])
            ])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 71), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 72), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 73), reg, lgc)
        ])
        self.addBugSetLoc(self.L_H_CAT_EAT_BUG, wlc)





