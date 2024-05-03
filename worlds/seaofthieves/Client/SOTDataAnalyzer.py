

import json
import SOTWebCollector
import recursive_diff
import time

import UserInformation
from worlds.seaofthieves.Locations.Locations import WebLocation
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
from worlds.seaofthieves.Items.Items import ItemCollection

class SOTDataAnalyzerSettings:

    def __init__(self, details: UserInformation.SotAnalyzerDetails):
        self.details = details

    def isPirateMode(self) -> bool:
        return self.details.shipName == ""

    def isShipMode(self) -> bool:
        return not self.isPirateMode()

    def getShipName(self) -> int:
        return int(self.details.shipName)

class OldNewValues:
    old: int = 0
    new: int = 0

class SOTDataAnalyzer:
    counter = 0
    collector : SOTWebCollector
    settings : SOTDataAnalyzerSettings

    def __init__(self, userInfo: UserInformation.UserInformation):
        self.collector = SOTWebCollector.SOTWebCollector(userInfo.loginCreds)
        self.settings = SOTDataAnalyzerSettings(userInfo.analyzerDetails)
        self.trackedLocations: dict[int,LocDetails] = {}
        #maps item id -> idx -> value
        self.trackedLocationsData: dict[int,dict[int,OldNewValues]] = {}

        self.banned: dict[int,bool] = {}

    def __readElementFromWebLocation(self, web_location: WebLocation, json_data):

        if not web_location.webJsonIdentifier.valid:
            # The idea behind this is to allow checks that are not real checks to be incremented once they have started being tracked
            # EX "Item in your Pocket" is made up, so it gets incremented on read after initial population, triggering the item.
            #
            # Therefore, as long as the "Dont track until it should be" logic works, this code will reward fake items with specific conditions
            # at the correct moment during play (granted, it happens up to 'server polling time' after the check actually happens)

            SOTDataAnalyzer.counter = SOTDataAnalyzer.counter+1
            return SOTDataAnalyzer.counter

        v = None
        alignment = web_location.webJsonIdentifier.alignment
        accolade = web_location.webJsonIdentifier.accolade
        stat = web_location.webJsonIdentifier.stat
        sub_stat = web_location.webJsonIdentifier.substat
        if self.settings.isPirateMode():
            v = json_data['Pirate']['Alignments'][alignment]['Accolades'][accolade]['Stats'][stat]
        else:
            v = json_data['Ships'][self.settings.getShipName()]['Alignments'][alignment]['Accolades'][accolade]['Stats'][stat]

        if sub_stat < 0:
            return v['Value']
        else:
            try:
                return v['SubStats'][sub_stat]['Value']
            except:
                print("Error: Web Parser: Please submit bug report for fix, this 'check' needs to be tracked manually. Web Location not found for - " + str(web_location))
                SOTDataAnalyzer.counter = SOTDataAnalyzer.counter + 1
                return SOTDataAnalyzer.counter

    def stopTracking(self, key: int):
        del self.trackedLocations[key]
        del self.trackedLocationsData[key]
        self.banned[key] = True

        return

    # region Update
    def update(self) -> None:
        json_data = self.collector.getJson()
        self.__updateWebDataForAll(json_data)

    def __updateWebDataForAll(self, json_data) -> None:
        total_eaten = json_data['Pirate']['Alignments'][3]['Accolades'][1]['Stats'][0]
        print("Prov Eaten: " + str(total_eaten))
        for loc_det in self.trackedLocations.keys():
            self.__updateWebDataForLocation(self.trackedLocations[loc_det], json_data)

    def __updateWebDataForLocation(self, loc_details: LocDetails, json_data) -> None:

        #we need to check if at least 1 web location value has been updated
        idx = 0
        for web_loc in loc_details.webLocationCollection:
            value = self.__readElementFromWebLocation(web_loc, json_data)

            self.trackedLocationsData[loc_details.id][idx].new = value

            idx = idx+1
    # endregion

    # region Adding a Location
    def allowTrackingOfLocation(self, loc_detail: LocDetails):

        # do not add twice
        if(loc_detail.id in self.trackedLocations.keys()):
            return

        self.trackedLocations[loc_detail.id] = loc_detail
        self.__setInitialValueForLoc(loc_detail)

    def __setInitialValueForLoc(self, loc_detail: LocDetails) -> None:
        json_data = self.collector.getJson()
        idx = 0
        for web_loc in loc_detail.webLocationCollection:
            value = self.__readElementFromWebLocation(web_loc, json_data)

            if(loc_detail.id not in self.trackedLocationsData.keys()):
                self.trackedLocationsData[loc_detail.id] = {}

            oldNewVals: OldNewValues = OldNewValues()
            oldNewVals.old = value
            oldNewVals.new = value
            self.trackedLocationsData[loc_detail.id][idx] = oldNewVals
            idx = idx+1

    # endregion

    # region Get completed stuff



    def getAllCompletedChecks(self) -> dict[int, bool]:

        returndict = {}
        # location id to yes/no
        for locId in self.trackedLocationsData.keys():
            if locId in self.banned.keys():
                continue
            for index in self.trackedLocationsData[locId].keys():
                oldNewData: OldNewValues = self.trackedLocationsData[locId][index]
                if(oldNewData.old != oldNewData.new):
                    returndict[locId] = True

        return returndict


    # endregion
