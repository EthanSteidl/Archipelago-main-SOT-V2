

import json
import SOTWebCollector
import recursive_diff
import time
import typing

import UserInformation
from worlds.seaofthieves.Locations.Locations import WebLocation
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
from worlds.seaofthieves.Items.Items import ItemCollection

class SOTDataAnalyzerSettings:

    def __init__(self, details: UserInformation.SotAnalyzerDetails):
        self.details: UserInformation.SotAnalyzerDetails = details

    def get_name_ship(self) -> str | None:
        return self.details.get_ship()

    def get_name_pirate(self) -> str | None:
        return self.details.get_pirate()


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
        self.trackedLocations: typing.Dict[int,LocDetails] = {}
        #maps item id -> idx -> value
        self.trackedLocationsData: typing.Dict[int,typing.Dict[int,OldNewValues]] = {}

        self.banned: typing.Dict[int,bool] = {}

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


        #for each pirate
        if self.settings.get_name_pirate() is not None:
            v = json_data['Pirate']['Alignments'][alignment]['Accolades'][accolade]['Stats'][stat]
        elif self.settings.get_name_ship() is not None:
            v = json_data['Ships'][int(self.settings.get_name_ship())]['Alignments'][alignment]['Accolades'][accolade]['Stats'][stat]
        else:
            print("Error: Web Parser: No pirate Name or Ship Name defined")
            return 0

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



    def getAllCompletedChecks(self) -> typing.Dict[int, bool]:

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
