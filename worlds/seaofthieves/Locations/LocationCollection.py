from .Voyager.IslandVisited import VoyageIslandVisited,SettingsVoyageIslandVisited
from .Voyager.VoyageQuestGh import VoyageQuestGh,SettingsVoyageQuestGh
from .Voyager.VoyageQuestOos import VoyageQuestOos,SettingsVoyageQuestOos
from .Voyager.VoyageQuestMa import VoyageQuestMa,SettingsVoyageQuestMa
from .Voyager.VoyageQuestRor import VoyageQuestRor,SettingsVoyageQuestRor
from .Voyager.VoyageQuestAthena import VoyageQuestAthena,SettingsVoyageQuestAthena
from .Rouge.RogueQuestAll import RogueQuestAll,SettingsRogueQuestAll
from .Feared.FearedQuestSeaForts import FearedQuestSeaForts,SettingsFearedQuestSeaForts
from .Menu.QuestMenu import MenuQuestAll,SettingsMenuQuestAll
from .Locations import SOTLocation, WebLocation, LocDetails, DoRand
from .Hunter.ProvisionsCooked import BurntAboard, CookedAboard, Total
from .Hunter.ProvisionsEaten import EatenAboard
from ..Regions.Name import Name
from ..Options import SOTOptions
from .LocationOptions import LocationOptions
from .Seals import Seals
from ..Items.Items import ItemCollection
from .Goldseaker import TreasuresSold, Chests
from ..Configurations import SotOptionsDerived
from .Servant import Servant
from .Guardian import Guardian
from .IllFated import IllFated
from .Feared import CannonsFired

class LocationDetailsCollection:

    count = 0

    #this maps Settings Class -> [locName -> LocDets]
    checkTypeToLocDetail: dict[str, dict[str, LocDetails]] = {}
    options: SotOptionsDerived.SotOptionsDerived

    hintWebLocations: [LocDetails] = []

    def __init__(self):
        LocDetails.resetSeedId()
        self.options = SotOptionsDerived.SotOptionsDerived()


    def getLocationForSeals(self, player, world) -> list[SOTLocation]:

        lst: list[SOTLocation] = []
        for locName in self.checkTypeToLocDetail["SettingsSeals"].keys():

            loc_det: LocDetails = self.checkTypeToLocDetail["SettingsSeals"][locName]

            reg = world.get_region(loc_det.webLocationCollection.getFirstRegion(), player)
            sot_loc = SOTLocation(loc_det, player, reg, None)

            reg.locations.append(sot_loc)

            lst.append(sot_loc)
        return lst



    def getLocCount(self):
        return self.count

    def toDict(self) -> dict[str, int]:
        dic: dict[str, int] = {}
        for checkTypeKey in self.checkTypeToLocDetail.keys():
            for loc_name in self.checkTypeToLocDetail[checkTypeKey].keys():
                dic[self.checkTypeToLocDetail[checkTypeKey][loc_name].name] = self.checkTypeToLocDetail[checkTypeKey][loc_name].id

        return dic

    def toDictAllPossible(self) -> dict[str,int]:

        #TODO this will cause items not in the randomizer to not be in the spoiler log,
        #should probably change this to be the complete list
        return self.toDict()


    def findDetailsCheckable(self, itemSet: set[str]) -> list[LocDetails]:

        #TODO check region reqs as well

        ret_list: list[LocDetails] = []

        #checks onlys location requirements, does not includ region reqs
        for checkTypeKey in self.checkTypeToLocDetail.keys():
            for loc_name in self.checkTypeToLocDetail[checkTypeKey].keys():
                loc_details = self.checkTypeToLocDetail[checkTypeKey][loc_name]
                if(loc_details.webLocationCollection.isAnyReachable(itemSet)):
                    ret_list.append(loc_details)


        return ret_list


    def addLocationToSelf(self, location_detail: LocDetails, settingsClass: str):


        if settingsClass not in self.checkTypeToLocDetail.keys():
            self.checkTypeToLocDetail[settingsClass] = {}

        self.checkTypeToLocDetail[settingsClass][location_detail.name] = location_detail

        self.count = self.count + 1

    def addHintToSelf(self, location_detail: LocDetails, settingsClass: str):
        self.hintWebLocations.append(location_detail)



    def addLocationsToSelf(self, lst: list[LocDetails], settingsClass: str):
        for i in range(len(lst)):
            self.addLocationToSelf(lst[i], settingsClass)

    def addHintsToSelf(self, lst: list[LocDetails], settingsClass: str):
        for i in range(len(lst)):
            self.addHintToSelf(lst[i], settingsClass)

    def getLocationsForRegion(self, regName: str, player: int) -> list[SOTLocation]:

        lst: list[SOTLocation] = []
        for settingString in self.checkTypeToLocDetail.keys():
            for locName in self.checkTypeToLocDetail[settingString].keys():

                loc_det: LocDetails = self.checkTypeToLocDetail[settingString][locName]
                if loc_det.webLocationCollection.getFirstRegion() == regName:
                    lst.append(SOTLocation(loc_det, player, regName))
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
        self.addGoldSeakerChests()
    def addGoldSeakerTreasuresSold(self):
        self.addLocationsToSelf(TreasuresSold.TreasuresSold().getLocations(), "SettingsTreasuresSold")
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
        self.addLocationsToSelf(VoyageQuestGh().getLocations(), "SettingsVoyageQuestGh")

    def addVoyageQuestMa(self):
        self.addLocationsToSelf(VoyageQuestMa().getLocations(), "SettingsVoyageQuestMa")

    def addVoyageQuestOos(self):
        self.addLocationsToSelf(VoyageQuestOos().getLocations(), "SettingsVoyageQuestOos")

    def addVoyageQuestRor(self):
        self.addLocationsToSelf(VoyageQuestRor().getLocations(), "SettingsVoyageQuestRor")

    def addVoyageQuestAthena(self):
        self.addLocationsToSelf(VoyageQuestAthena().getLocations(), "SettingsVoyageQuestAthena")
    # endregion

    # region Rouge
    def addAllRouge(self):
        self.addLocationsToSelf(RogueQuestAll().getLocations(), "SettingsRogueQuestAll")
    # endregion


    # region Hunter
    def addAllHunter(self):
        self.addHunterBurnt()
        self.addHunterCooked()
        self.addHunterTotal()
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
        self.addLocationsToSelf(FearedQuestSeaForts().getLocations(), "SettingsFearedQuestSeaForts")
    # endregion

