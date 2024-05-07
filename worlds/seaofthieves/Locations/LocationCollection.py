from .Voyager.IslandVisited import VoyageIslandVisited
from .Voyager.VoyageQuestGh import VoyageQuestGh
from .Voyager.VoyageQuestOos import VoyageQuestOos
from .Voyager.VoyageQuestMa import VoyageQuestMa
from .Voyager.VoyageQuestRor import VoyageQuestRor
from .Voyager.VoyageQuestAthena import VoyageQuestAthena
from .Rouge.RogueQuestAll import RogueQuestAll
from .Feared.FearedQuestSeaForts import FearedQuestSeaForts
from .Menu.QuestMenu import MenuQuestAll
from .Locations import SOTLocation, LocDetails
from .Hunter.ProvisionsCooked import BurntAboard, CookedAboard, Total
from .Hunter.ProvisionsEaten import EatenAboard
from .Seals import Seals
from .Goldseaker import TreasuresSold, Chests
from ..Configurations import SotOptionsDerived
from .Servant import Servant
from .Guardian import Guardian
from .IllFated import IllFated
from .Feared import CannonsFired
from ..Regions.RegionConnectionRules import ConnectionDetails
import typing
class LocationDetailsCollection:


    def __init__(self):
        LocDetails.resetSeedId()
        self.options: SotOptionsDerived.SotOptionsDerived = SotOptionsDerived.SotOptionsDerived()

        self.count = 0

        # this maps Settings Class -> [locName -> LocDets]
        self.checkTypeToLocDetail: typing.Dict[str, typing.Dict[str, LocDetails]] = {}

        self.hintWebLocations: [LocDetails] = []

    def getLocCount(self):
        return self.count

    def toDict(self) -> typing.Dict[str, int]:
        dic: typing.Dict[str, int] = {}
        for checkTypeKey in self.checkTypeToLocDetail.keys():
            for loc_name in self.checkTypeToLocDetail[checkTypeKey].keys():
                dic[self.checkTypeToLocDetail[checkTypeKey][loc_name].name] = self.checkTypeToLocDetail[checkTypeKey][loc_name].id

        return dic

    def isRegionAccessibleForLocation(self, loc_details: LocDetails):

        #TODO implement region logic. The idea is to use the Region Connection Rules here to keep track of accessible regions

        return True


        #if we have a table like this we can solve the problem
        # [list]
        # at idx = (Region name of to, Region name of from, set of required items)
        # then we can double loop this table to mark off locations reachable
        # algorithm finishes once no more locations are marked off
    def findDetailsCheckable(self, itemSet: typing.Set[str], forceAll: bool = False) -> typing.List[LocDetails]:

        ret_list: typing.List[LocDetails] = []

        #checks onlys location requirements, does not includ region reqs
        for checkTypeKey in self.checkTypeToLocDetail.keys():
            for loc_name in self.checkTypeToLocDetail[checkTypeKey].keys():

                loc_details = self.checkTypeToLocDetail[checkTypeKey][loc_name]

                #first check if we have access to the region
                if forceAll or self.isRegionAccessibleForLocation(loc_details):
                    #then check item logic
                    if(forceAll or loc_details.webLocationCollection.isAnyReachable(itemSet)):
                        ret_list.append(loc_details)


        return ret_list


    def addLocationToSelf(self, location_detail: LocDetails, settingsClass: str):


        if settingsClass not in self.checkTypeToLocDetail.keys():
            self.checkTypeToLocDetail[settingsClass] = {}

        self.checkTypeToLocDetail[settingsClass][location_detail.name] = location_detail

        self.count = self.count + 1

    def addHintToSelf(self, location_detail: LocDetails, settingsClass: str):
        self.hintWebLocations.append(location_detail)



    def addLocationsToSelf(self, lst: typing.List[LocDetails], settingsClass: str):
        for i in range(len(lst)):
            self.addLocationToSelf(lst[i], settingsClass)

    def addHintsToSelf(self, lst: typing.List[LocDetails], settingsClass: str):
        for i in range(len(lst)):
            self.addHintToSelf(lst[i], settingsClass)

    def getLocationsForRegion(self, regName: str, player: int) -> typing.List[SOTLocation]:

        lst: typing.List[SOTLocation] = []
        for settingString in self.checkTypeToLocDetail.keys():
            for locName in self.checkTypeToLocDetail[settingString].keys():

                loc_det: LocDetails = self.checkTypeToLocDetail[settingString][locName]
                if loc_det.webLocationCollection.getFirstRegion() == regName:
                    loc = SOTLocation(loc_det, player, regName)
                    if not loc_det.doRandomize:
                        loc.progress_type = 3 #excluded
                    lst.append(loc)
        return lst

    def applyOptions(self, options: SotOptionsDerived.SotOptionsDerived):
        self.options = options
        return



    def addAll(self) -> None:
        self.addMenuQuest()
        self.addVoyageQuestGh()
        self.addVoyageQuestMa()
        self.addVoyageQuestOos()
        self.addVoyageQuestRor()
        self.addVoyageQuestAthena()

        self.addAllGoldSeaker()
        self.addAllHunter()
        self.addAllFeared()
        self.addAllRouge()
        self.addAllGuardian()
        self.addAllServant()
        self.addAllIllFated()

        self.addSeals()

        #hints?
        self.addIslandVisited()

        return


    def addAllIllFated(self):
        self.addLocationsToSelf(IllFated.IllFated(self.options.illFatedSettings).getLocations(), "SettingsIllFated")
    def addAllServant(self):
        self.addLocationsToSelf(Servant.VoyageQuestSv(self.options.servantSettings).getLocations(), "SettingsVoyageQuesSv")

    def addAllGuardian(self):
        self.addLocationsToSelf(Guardian.VoyageQuestGa(self.options.guardianSettings).getLocations(), "SettingsVoyageQuesGa")


    def addAllGoldSeaker(self):
        self.addGoldSeakerTreasuresSold()

        #TODO this is buggy
        #self.addGoldSeakerChests()
    def addGoldSeakerTreasuresSold(self):
        self.addLocationsToSelf(TreasuresSold.TreasuresSold(self.options.treasureSoldSettings).getLocations(), "SettingsTreasuresSold")
    def addGoldSeakerChests(self):
        self.addLocationsToSelf(Chests.Chests(self.options.chestSettings).getLocations(), "SettingsChests")

    def addSeals(self):
        self.addLocationsToSelf(Seals.Seals().getLocations(), "SettingsSeals")

    def addMenuQuest(self):

        self.addLocationsToSelf(MenuQuestAll().getLocations(), "SettingsMenuQuestAll")

    # region voyages
    def addIslandVisited(self):
        self.addHintsToSelf(VoyageIslandVisited().getLocations(), "HintsIslandsVisited")

    def addVoyageQuestGh(self):
        self.addLocationsToSelf(VoyageQuestGh(self.options.voyageQuestGhSettings).getLocations(), "SettingsVoyageQuestGh")

    def addVoyageQuestMa(self):
        self.addLocationsToSelf(VoyageQuestMa(self.options.voyageQuestMaSettings).getLocations(), "SettingsVoyageQuestMa")

    def addVoyageQuestOos(self):
        self.addLocationsToSelf(VoyageQuestOos(self.options.voyageQuestOosSettings).getLocations(), "SettingsVoyageQuestOos")

    def addVoyageQuestRor(self):
        self.addLocationsToSelf(VoyageQuestRor(self.options.voyageQuestRorSettings).getLocations(), "SettingsVoyageQuestRor")

    def addVoyageQuestAthena(self):
        self.addLocationsToSelf(VoyageQuestAthena(self.options.voyageQuestAthenaSettings).getLocations(), "SettingsVoyageQuestAthena")
    # endregion

    # region Rouge
    def addAllRouge(self):
        self.addLocationsToSelf(RogueQuestAll(self.options.rougeSettings).getLocations(), "SettingsRogueQuestAll")
    # endregion


    # region Hunter
    def addAllHunter(self):
        self.addHunterBurnt()
        self.addHunterCooked()
        #self.addHunterTotal() #This should probably be deleted
        self.addHunterEaten()

    def addHunterBurnt(self):
        self.addLocationsToSelf(BurntAboard.HunterBurntAboard(self.options.burntAboardSettings).getLocations(),
                                "SettingsHunterBurntAboard")

    def addHunterCooked(self):
        self.addLocationsToSelf(CookedAboard.HunterCookedAboard(self.options.cookedAboardSettings).getLocations(), "SettingsHunterCookedAboard")

    def addHunterTotal(self):
        self.addLocationsToSelf(Total.HunterTotal().getLocations(), "SettingsHunterTotalCooked")

    def addHunterEaten(self):
        self.addLocationsToSelf(EatenAboard.HunterEatenAboard(self.options.eatenAboardSettings).getLocations(), "SettingsHunterEatenAboard")

    # endregion

    # region Feared

    def addAllFeared(self):
        self.addFearedQuestSeaForts()
        self.addLocationsToSelf(CannonsFired.CannonsFired(self.options.cannonsFiredSettings).getLocations(), "SettingsCannonsFired")

    def addFearedQuestSeaForts(self):
        self.addLocationsToSelf(FearedQuestSeaForts(self.options.fortressSettings).getLocations(), "SettingsFearedQuestSeaForts")
    # endregion

