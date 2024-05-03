from __future__ import annotations
# CommonClient import first to trigger ModuleUpdater
import json
import multiprocessing

from worlds.seaofthieves.Locations.Locations import WebLocation
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
from worlds.seaofthieves.Items.Items import ItemCollection

import Shop
import PlayerInventory
import asyncio
import copy
import json
import logging
import os
import random
import re
import string
import subprocess
import sys
import time
import typing
from queue import Queue
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser
from Utils import init_logging, is_windows, async_start
import sys
import threading
import SOTDataAnalyzer
import typing
from NetUtils import ClientStatus, NetworkItem, JSONtoTextParser, JSONMessagePart, add_json_item, add_json_location, add_json_text, JSONTypes
import UserInformation
import argparse
import time
import asyncio
import multiprocessing
import logging
import Utils
from typing import NamedTuple
from worlds.seaofthieves.Client.NetworkProtocol.PrintJsonPacket import PrintJsonPacket
from worlds.seaofthieves.Client.NetworkProtocol.ReceivedItemsPacket import ReceivedItemsPacket
class Version(NamedTuple):
    major: int
    minor: int
    build: int
import socket

async def watchGameForever(ctx):
    firstpass = True
    while True:

        if ctx.connected_to_server:
            if firstpass:
                firstpass = False
            else:
                try:
                    ctx.updateAnalyzerWithLocationsPossible()
                    await ctx.collectLocationsAndSendInformation()
                except Exception as e:
                    print("Fatal error occured: ", e)

        await asyncio.sleep(4)

class SOT_CommandProcessor(ClientCommandProcessor):
    ctx: SOT_Context

    def _cmd_pog(self, st: str = "") -> bool:

        self.output("we pog")

        return True

    def _cmd_poggin(self) -> bool:

        self.output("bring deathssss")

        return True

    def _cmd_linkShip(self, command: str) -> bool:
        print("Not Implemented")
        return False

        #command in form "shipName<->mscookie"
        args = command.split("<->")
        if len(args) < 2:
            print("Invalid argument count of " + str(len(args)) + ". Expected 2.")
            return False

        shipName = args[0]
        msCookie = args[1]
        self.ctx.analyzer.addShip(shipName, msCookie)
        return True
    def _cmd_linkPirate(self, command: str) -> bool:
        print("Not Implemented")
        return False

        #command in form "shipName<->mscookie"
        args = command.split("<->")
        if len(args) < 2:
            print("Invalid argument count of " + str(len(args)) + ". Expected 2.")
            return False

        name = args[0]
        msCookie = args[1]
        self.ctx.analyzer.addPirate(name, msCookie)
        return True

    def _cmd_shop(self) -> bool:
        self.ctx.shop.info(self.ctx.playerInventory)
        return True

    def _cmd_buy(self, menu_line_number):
        menu_line_number = str(menu_line_number)
        self.ctx.shop.executeAction(menu_line_number, self.ctx.playerInventory)




class SOT_Context(CommonContext):
    command_processor = SOT_CommandProcessor


    def __init__(self, serverAddress: str | None, serverPassword: str | None, userInformation: UserInformation.UserInformation):
        super().__init__(serverAddress, serverPassword)
        self.userInformation = userInformation
        self.analyzer: SOTDataAnalyzer.SOTDataAnalyzer = SOTDataAnalyzer.SOTDataAnalyzer(userInformation)
        self.known_items_received = [] #used to track measured received counts

        self.locationDetailsCollection = LocationDetailsCollection()
        self.locationDetailsCollection.addAll()
        self.discoveryHints = {}

        self.itemCollection = ItemCollection()
        self.shop = Shop.Shop()
        self.playerInventory = PlayerInventory.PlayerInventory()
        self.connected_to_server = False


    def updateClientStatus(self, status: ClientStatus):
        self.send_msgs([{"cmd": 'StatusUpdate', "status": status}])

    def isItemUpdateForReceiving(self) -> bool:
        return len(self.known_items_received) < len(self.items_received)

    def processItemUpdateForClient(self) -> None:
        pass

    def _canReachWebLocation(self, currentItemIds: set[int], web_loc: WebLocation):
        pass

    def locationsReachableWithCurrentItems(self) -> list[LocDetails]:

        returnList: set[str] = set()
        currentItems: set[str] = set()

        # check out our current items
        for item in self.items_received:
            id = item.item
            name: str = self.itemCollection.getNameFromId(id)

            #if the name is null, there is a bug but we should handle it here
            if(name != ""):
                currentItems.add(name)


        return self.locationDetailsCollection.findDetailsCheckable(currentItems)


    def on_package(self, cmd: str, args: dict):
        if cmd == "RoomInfo":
            asyncio.create_task(fConnectToRoom(self), name="FConnecToRoom")

        elif cmd == "Connected":
            self.connected_to_server = True
            print("We have connected!!!!")
            self.discoveryHints = args["slot_data"]
            print(args)

        elif cmd == "LocationInfo":
            pass
            # TODO we should acknowledge the items have been recieved and stop sending them again

        elif cmd == "RoomUpdate":
            print("We got a room update")
            print(args)

        elif cmd == "Bounced":
            #do nothing
            pass

        elif cmd == "Retrieved":
            print("Retrieved packet?")
            print(args)

        elif cmd == "ReceivedItems":


            receivedItemsPacket: ReceivedItemsPacket = ReceivedItemsPacket(args)
            if(receivedItemsPacket.items is not None):
                self.items_received = receivedItemsPacket.items



        elif cmd == "PrintJSON":
            printJsonPacket: PrintJsonPacket = PrintJsonPacket(args)
            printJsonPacket.print()

        else:
            print("Error: Server requested unsupported feature '{0}'".format(cmd))

            #this is where you read slot data if any





    def acknowledgeItemsReceived(self):
        for itm in self.items_received:
            if(itm not in self.known_items_received):
                print("Server gave us -> " + str(itm.item))
        self.known_items_received = self.items_received

    def getAndClearNewLocationsReached(self) -> set[int]:
        locations: set[int] = set()
        checks = self.analyzer.getAllChecks()
        for locId, isChecked in checks.items():
            if(isChecked):
                locations.add(locId)

        return locations

    def updateAnalyzerWithLocationsPossible(self):

        loc_details_possible: list[LocDetails] = self.locationsReachableWithCurrentItems()
        for loc_detail in loc_details_possible:
            self.analyzer.allowTrackingOfLocation(loc_detail)
        self.acknowledgeItemsReceived()

    async def collectLocationsAndSendInformation(self):

        # Sync server itmes to us
        await self.send_msgs([
            {
                "cmd": "Sync"
            }
        ])

        # Use those items to check if we can finish anything
        self.analyzer.update()
        completedChecks: dict[int, bool] = self.analyzer.getAllCompletedChecks()
        for k in completedChecks.keys():
            if completedChecks[k]:
                print("Completed -> " + str(k))
                self.locations_checked.add(k)
                self.analyzer.stopTracking(k)


        # inform server of what we can finish
        msg = [
            {
                "cmd": "LocationChecks",
                "locations": list(self.locations_checked)
            }
        ]
        await self.send_msgs(msg)
        msg = [
            {
                "cmd": "LocationScouts",
                "locations": list(self.locations_checked)
            }
        ]
        await self.send_msgs(msg)










def getSeaOfThievesDataFromArguments() -> UserInformation.UserInformation:
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', dest='address', type=str, help='ip address : port of host')
    parser.add_argument('--ship', dest='ship', type=str, help='Player ship name')
    parser.add_argument('--user', dest='username', type=str, help='Player username')
    parser.add_argument('--mscookie', dest='msCookie', type=str,
                        help='Microsoft login cookie given to www.seaofthieves.com', nargs='+')
    args = parser.parse_args()

    if( args.address is None or args.ship is None or args.msCookie is None):
        print("Error: Expected 3 command line arguments")
        print("Required \"--address <ipaddress:port>\"")
        print("Required \"--ship <shipNumber>\"")
        print("Required \"--mscookie <cookie>\"")
        print("Example Command: python SotCustomClient.py --address 127.0.0.1:25255 --ship 1 --mscookie 1j23iuo1j23p1h2j3p1h")
        print("To run this file you must have ptyhon installed, then modify the command line arguments of this executable to the above. The address is the connection address of the server. The ship param is the ship number you want to monitor. The MSCOOKIE is your microsoft auth cookie.")
        exit()

    sotLoginCredentials: UserInformation.SotLoginCredentials = UserInformation.SotLoginCredentials(' '.join(args.msCookie))
    sotAnalyzerDetails: UserInformation.SotAnalyzerDetails = UserInformation.SotAnalyzerDetails(args.ship, None)
    userInfo = UserInformation.UserInformation(sotLoginCredentials, sotAnalyzerDetails, args.address, args.username)
    return userInfo

async def every(__seconds: float, func, *args, **kwargs):
    while True:
        func(*args, **kwargs)
        await asyncio.sleep(__seconds)




class RunningCli(threading.Thread):
    def __init__(self, sharedContext, *args, **kwargs):
        super(RunningCli,self).__init__(*args, **kwargs)
        self.sharedContext: SOT_Context = sharedContext

    async def runCli(self):
        print("running cli")
        self.sharedContext.run_cli()
        await self.sharedContext.exit_event.wait()

    def run(self):
        asyncio.run(self.runCli())


from typing import NamedTuple
class Version(NamedTuple):
    major: int
    minor: int
    build: int
async def fConnectToRoom(ctx : SOT_Context):

    username = ctx.userInformation.username
    await ctx.send_msgs([
        {
            "cmd": "Connect",
            "game": "Sea of Thieves",
            "password": "",
            "name": username,
            "uuid": username,
            "items_handling": 0b111,
            "slot_data": True,
            "tags": [],
            "version": Version(1,1,1)
        }
    ])
    return

async def game_watcher(ctx: SOT_Context):
    logger = logging.getLogger("SOT_watcher")

    try:
        while not ctx.exit_event.is_set():
            logger.warning("This is my warning!!")
            ctx.getUpdatesBasedOnItemsReceived()
            ctx.sendUpdatesBasedOnItemsFound()
            await asyncio.sleep(2)
    except:
        pass



async def main():
    Utils.init_logging("Sea of Thieves")
    multiprocessing.freeze_support()
    user_info: UserInformation.UserInformation = getSeaOfThievesDataFromArguments()
    ctx = SOT_Context(user_info.address, None, user_info)
    await ctx.connect(user_info.address)

    ctx.run_cli()
    f = asyncio.create_task(watchGameForever(ctx), name="ever")

    await ctx.exit_event.wait()
    #await progression_watcher
    await f
    await ctx.shutdown()
    return



if __name__ == '__main__':
    asyncio.run(main())

