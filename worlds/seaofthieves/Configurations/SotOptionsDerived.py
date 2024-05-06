import typing

from ..Options import SOTOptions
from ..Locations.Feared import FearedQuestSeaForts, CannonsFired
from ..Locations.Hunter.ProvisionsCooked import BurntAboard
from ..Locations.Hunter.ProvisionsCooked import CookedAboard
from ..Locations.Hunter.ProvisionsEaten import EatenAboard
from ..Locations.Servant import Servant
from ..Locations.Seals import Seals
from ..Locations.Menu import QuestMenu
from ..Locations.Guardian import Guardian
from ..Locations.IllFated import IllFated
from ..Locations.Goldseaker import Chests
class SotOptionsDerived:


    def __init__(self, sotOptions: typing.Optional[SOTOptions] = None):
        self.burntAboardSettings: BurntAboard.SettingsHunterBurntAboard
        self.cookedAboardSettings: CookedAboard.SettingsHunterCookedAboard
        self.eatenAboardSettings: EatenAboard.SettingsHunterEatenAboard
        self.servantSettings: Servant.SettingsVoyageQuestSv
        self.fortressSettings: FearedQuestSeaForts.SettingsFearedQuestSeaForts
        self.sealsSettings: Seals.SettingsSeals
        self.menuSettings: QuestMenu.SettingsMenuQuestAll
        self.guardianSettings: Guardian.SettingsVoyageQuestGa
        self.illFatedSettings: IllFated.SettingsIllFated
        self.cannonsFiredSettings: CannonsFired.SettingsCannonsFired
        self.chestSettings: Chests.SettingsChest

        if(sotOptions == None):
            self.burntAboardSettings = BurntAboard.SettingsHunterBurntAboard()
            self.cookedAboardSettings = CookedAboard.SettingsHunterCookedAboard()
            self.eatenAboardSettings = EatenAboard.SettingsHunterEatenAboard()
            self.servantSettings = Servant.SettingsVoyageQuestSv()
            self.fortressSettings = FearedQuestSeaForts.SettingsFearedQuestSeaForts()
            self.sealsSettings = Seals.SettingsSeals()
            self.menuSettings = QuestMenu.SettingsMenuQuestAll()
            self.guardianSettings = Guardian.SettingsVoyageQuestGa()
            self.illFatedSettings = IllFated.SettingsIllFated()
            self.cannonsFiredSettings = CannonsFired.SettingsCannonsFired()
            self.chestSettings = Chests.SettingsChest()
        else:
            self.burntAboardSettings = self.__getBurntAboardSettings(sotOptions)
            self.cookedAboardSettings = self.__getCookedAboardSettings(sotOptions)
            self.eatenAboardSettings = self.__getEatenAboardSettings(sotOptions)
            self.servantSettings = self.__getServantSettings(sotOptions)
            self.fortressSettings = self.__getFortressSettings(sotOptions)
            self.sealsSettings = self.__getSealsSettings(sotOptions)
            self.menuSettings = self.__getMenuSettings(sotOptions)
            self.guardianSettings = self.__getGuadianSettings(sotOptions)
            self.illFatedSettings = self.__getIllFatedSettings(sotOptions)
            self.cannonsFiredSettings = self.__getCannonsFiredSettings(sotOptions)
            self.chestSettings = self.__getChestSettings(sotOptions)

    def __getChestSettings(self, sotOptions: SOTOptions):
        gh_count: int = sotOptions.sellSettingsGh
        ma_count: int = sotOptions.sellSettingsMa
        oos_count: int = sotOptions.sellSettingsOos
        af_count: int = sotOptions.sellSettingsAf
        rb_count: int = sotOptions.sellSettingsRb

        return Chests.SettingsChest(gh_count, ma_count, oos_count, rb_count, af_count)



    def __getCannonsFiredSettings(self, sotOptions: SOTOptions):

        balls: int = int(sotOptions.cannonSanityBalls)
        cursed: int = int(sotOptions.cannonSanityCursed)
        phantom: int = int(sotOptions.cannonSanityPhantom)

        return CannonsFired.SettingsCannonsFired(balls, cursed, phantom)
    def __getIllFatedSettings(self, sotOptions: SOTOptions):
        return IllFated.SettingsIllFated(sotOptions.illFated)
    def __getGuadianSettings(self, sotOptions: SOTOptions):
        compAny: int
        sloop: int
        brig: int
        gal: int

        if(sotOptions.guardianSanity == 2):
            compAny = 0
            sloop = 1
            brig = 1
            gal = 1
        elif(sotOptions.guardianSanity == 1):
            compAny = 1
            sloop = 0
            brig = 0
            gal = 0
        else:
            compAny = 0
            sloop = 0
            brig = 0
            gal = 0

        return Guardian.SettingsVoyageQuestGa(compAny, sloop, brig, gal)

    def __getMenuSettings(self, sotOptions: SOTOptions):
        sealCount: int = sotOptions.sealCount
        return QuestMenu.SettingsMenuQuestAll(sealCount)

    def __getSealsSettings(self, sotOptions: SOTOptions):
        return Seals.SettingsSeals()

    def __getFortressSettings(self, sotOptions: SOTOptions):
        completeAny: int = 0
        royal: int = 0
        imp: int = 0
        gold: int = 0
        brine: int = 0
        traitor: int = 0
        mercy: int = 0

        if(sotOptions.fortressSanity == 0):
            pass
        elif(sotOptions.fortressSanity == 1):
            completeAny = 1
        elif(sotOptions.fortressSanity == 2):
            royal = 1
            imp = 1
            gold = 1
            brine = 1
            traitor = 1
            mercy = 1

        return FearedQuestSeaForts.SettingsFearedQuestSeaForts(completeAny, royal, imp, gold, brine, traitor, mercy)

    def __getBurntAboardSettings(self, sotOptions: SOTOptions):
        compAny: int = 1
        fish: int = int(sotOptions.burnSanityFish)
        seamonster: int = int(sotOptions.burnSanitySeamonster)
        landAnimal: int = int(sotOptions.burnSanityLandAnimal)

        #if we have foodsanity on, we dont want a generic check if we want specific things
        if( fish + seamonster + landAnimal > 0):
            compAny = 0

        return BurntAboard.SettingsHunterBurntAboard(compAny, fish, landAnimal, seamonster)

    def __getCookedAboardSettings(self, sotOptions: SOTOptions):
        compAny: int = 1
        fish: int = int(sotOptions.cookSanityFish)
        seamonster: int = int(sotOptions.cookSanitySeamonster)
        landAnimal: int = int(sotOptions.cookSanityLandAnimal)

        # if we have foodsanity on, we dont want a generic check if we want specific things
        if (fish + seamonster + landAnimal > 0):
            compAny = 0

        return CookedAboard.SettingsHunterCookedAboard(compAny, fish, landAnimal, seamonster)

    def __getEatenAboardSettings(self, sotOptions: SOTOptions):
        compAny: int = 1
        fish: int = int(sotOptions.foodSanityFish)
        seamonster: int = int(sotOptions.foodSanitySeamonster)
        landAnimal: int = int(sotOptions.foodSanityLandAnimal)
        bug: int = int(sotOptions.foodSanityBug)
        fruit: int = int(sotOptions.foodSanityFruit)

        # if we have foodsanity on, we dont want a generic check if we want specific things
        if (fish + seamonster + landAnimal + bug + fruit> 0):
            compAny = 0

        return EatenAboard.SettingsHunterEatenAboard(compAny, fish, landAnimal, seamonster, fruit, bug)

    def __getServantSettings(self, sotOptions: SOTOptions):
        compAny: int
        sloop: int
        brig: int
        gal: int

        if(sotOptions.servantSanity == 2):
            compAny = 0
            sloop = 1
            brig = 1
            gal = 1
        elif(sotOptions.servantSanity == 1):
            compAny = 1
            sloop = 0
            brig = 0
            gal = 0
        else:
            compAny = 0
            sloop = 0
            brig = 0
            gal = 0

        return Servant.SettingsVoyageQuestSv(compAny, sloop, brig, gal)
