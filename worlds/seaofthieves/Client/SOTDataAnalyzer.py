

import json
import time

import worlds.seaofthieves.Client.SOTWebCollector as SOTWebCollector
import typing

import worlds.seaofthieves.Client.UserInformation as UserInformation
from worlds.seaofthieves.Locations.Locations import WebLocation
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
from worlds.seaofthieves.Items.Items import ItemCollection
import worlds.seaofthieves.Client.Balance as Balance
from worlds.seaofthieves.Client.windowcapture import  WindowCapture
import pytesseract
import cv2

class SOTDataAnalyzerSettings:

    def __init__(self, details: UserInformation.SotAnalyzerDetails):
        self.details: UserInformation.SotAnalyzerDetails = details

    def get_name_ship(self) -> typing.Optional[str]:
        return self.details.get_ship()

    def get_name_pirate(self) -> typing.Optional[str]:
        return self.details.get_pirate()


class OldNewValues:
    old: int = 0
    new: int = 0

class SOTDataAnalyzer:
    counter = 0
    collector : SOTWebCollector
    settings : SOTDataAnalyzerSettings

    #TODO this is going to need to work for other people...
    install_folder = r'C:\Users\Ethan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = install_folder

    def __init__(self, userInfo: UserInformation.UserInformation, queryperiod: typing.Optional[int] = None):
        self.collector = SOTWebCollector.SOTWebCollector(userInfo.loginCreds, queryperiod)
        self.settings = SOTDataAnalyzerSettings(userInfo.analyzerDetails)
        self.trackedLocations: typing.Dict[int,LocDetails] = {}
        #maps item id -> idx -> value
        self.trackedLocationsData: typing.Dict[int,typing.Dict[int,OldNewValues]] = {}

        self.banned: typing.Dict[int,bool] = {}
        self.window_capture: WindowCapture = WindowCapture("Sea of Thieves")
        self.window_capture.list_window_names()
        self.last_screenshot_time = -1000
        self.screenshot_second_interval = 2
        self.screen_text = ""
        self.screen_image_bw = None
        self.screen_image_grey = None
        self.scr_success = True


    def __readElementFromScreenText(self, web_location: WebLocation) -> bool:

        #check if there is a screen element on the web location
        if web_location.screenData is None:
            return False

        if self.last_screenshot_time + self.screenshot_second_interval < time.time():
            self.last_screenshot_time = time.time()

            try:
                # C:\Users\Ethan\AppData\Local\Programs\Tesseract - OCR

                self.screen_image_bw, self.screen_image_grey = self.window_capture.get_screenshot_2()
                #self.screen_image_bw.show()
                # pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
                self.screen_image_grey.save("screen_cap.png")

                self.screen_text = pytesseract.image_to_string(self.screen_image_bw,config='--psm 3').lower()
                # if self.screen_text == "":
                #     print("No Text Found")
                # else:
                #     print(self.screen_text)
                if self.scr_success == False:
                    print("Game window found!")
                self.scr_success = True
            except Exception as e:


                #we just could not find the window
                if self.scr_success:
                    print("Game window not found - report as bug if game is running")
                self.scr_success = False

        if web_location.screenData.hasMatch(self.screen_text, self.screen_image_grey):
            return True

        return False

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


        try:
            read_element = v
            if sub_stat >= 0:
                v = v['SubStats'][sub_stat]
            json_name = v['LocalisedTitle']
            value = v['Value']

            # check to see if the api has updated the substat location. If it did, try to figure out what location to read from in the meantime
            if sub_stat >= 0 and web_location.webJsonIdentifier.json_name is not None and web_location.webJsonIdentifier.json_name != json_name:
                for secondary_sub_stat in read_element['SubStats'].keys():
                    secondary_json_name = read_element['SubStats'][secondary_sub_stat]['LocalisedTitle']
                    secondary_value = read_element['SubStats'][secondary_sub_stat]['Value']

                    if secondary_json_name == web_location.webJsonIdentifier.json_name:
                        loc_ids = "{} {} {} {}".format(alignment, accolade, stat, sub_stat)
                        web_location.webJsonIdentifier.stat = secondary_sub_stat
                        #print("Warning: Web Parser: {} at {} has name {}, but we found {} at {}, using this instead.".format(web_location.webJsonIdentifier.json_name, loc_ids, json_name, secondary_json_name, secondary_value))
                        return secondary_value



            return value

        except:
            print("Error: Web Parser: Please submit bug report for fix, this location will be awarded to the correct player right now. Web Location not found for - " + "{} {} {} {}".format(alignment, accolade, stat, sub_stat))

            # The idea here is to award the player for completing the check
            SOTDataAnalyzer.counter = SOTDataAnalyzer.counter + 1
            return SOTDataAnalyzer.counter

    def stopTracking(self, key: int):
        self.trackedLocations.pop(key, None)
        self.trackedLocationsData.pop(key, None)
        self.banned[key] = True
        print("banned ",key)

        return

    # region Update
    def update(self) -> None:
        json_data = self.collector.getJson()
        self.__updateWebDataForAll(json_data)

    def __updateWebDataForAll(self, json_data) -> None:
        for loc_det in self.trackedLocations.keys():
            self.__updateWebDataForLocation(self.trackedLocations[loc_det], json_data)

    def __updateWebDataForLocation(self, loc_details: LocDetails, json_data) -> None:

        #just make sure we are not banned
        if loc_details.id in self.banned.keys():
            return

        #we need to check if at least 1 web location value has been updated
        idx = 0
        for web_loc in loc_details.webLocationCollection:
            scrren_caped = False
            try:
                scrren_caped = self.__readElementFromScreenText(web_loc)
            except Exception as e:
                print("Fatal Error: " + str(e))
            if scrren_caped:
                #then we detected the check event
                self.trackedLocationsData[loc_details.id][idx].new = self.trackedLocationsData[loc_details.id][idx].old + 1
            elif not web_loc.ocr_only:
                #since the screen event is likely faster, we need to account for that here
                value = self.__readElementFromWebLocation(web_loc, json_data)
                if value < self.trackedLocationsData[loc_details.id][idx].new:
                    # we know it was updated in a different way
                    pass
                else:
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

    def getBalance(self) -> Balance.Balance:
        js: json = self.collector.getBalance()
        return Balance.fromJson(js)


