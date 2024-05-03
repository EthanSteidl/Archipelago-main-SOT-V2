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
                ctx.updateAnalyzerWithLocationsPossible()
                await ctx.collectLocationsAndSendInformation()

        await asyncio.sleep(4)

class SOT_CommandProcessor(ClientCommandProcessor):
    ctx: SOT_Context

    def _cmd_pog(self, st: str = "") -> bool:

        self.output("we pog")

        return True

    def _cmd_poggin(self) -> bool:

        self.output("bring deathssss")

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
        print("...Checking if checks have been completed")

        loc_details_possible: list[LocDetails] = self.locationsReachableWithCurrentItems()
        for loc_detail in loc_details_possible:
            self.analyzer.allowTrackingOfLocation(loc_detail)
        self.acknowledgeItemsReceived()

    async def collectLocationsAndSendInformation(self):
        print(".....Sending completed checks to server")

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
    parser.add_argument('--mscookie', dest='msCookie', type=str,
                        help='Microsoft login cookie given to www.seaofthieves.com', nargs='+')
    args = parser.parse_args()

    if( args.address is None or args.ship is None or args.msCookie is None):
        print("Error: Expected 3 command line arguments")
        print("Required \"--address <ipaddress:port>\"")
        print("Required \"--ship <shipNumber>\"")
        print("Required \"--mscookie <cookie>\"")
        print("Example Command: python SotCustomClient.py --address 127.0.0.1:25255 --ship 1 --mscookie 1j23iuo1j23p1h2j3p1h")
        exit()

    #args.msCookie = 'ARRAffinity=db6e5e3c8a73940baeb907fc9b4fa53ca3f5bc9c5f01f7925a6793df2f1ebe1e; ARRAffinitySameSite=db6e5e3c8a73940baeb907fc9b4fa53ca3f5bc9c5f01f7925a6793df2f1ebe1e; MSCC=NR; rat=eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiemlwIjoiREVGIn0..GCSEfDqP-YVcu5qyMXFIlw.h-6Eic0cixb-pv6iWMgbSJYIVSQ_QYWuuJWfLYpMdB_KTJuOEj0mK9wsLxTM8SajM6atRtMsciO7Ea7JlcghocblMwKYctxcO7NB-FaR2vUxXOOkSJwu3sy-npluLEhOp7ZF-6MCTj3GDNL2KDV1qsahIXZb55ilZrW34IeP_ym0j6F7TIxWNmhoNAJupJkllC2AAb0yJBwklGbQ1hO9bm7tLGBHQPp1XPEJNpcmxDNbQttE9B-rO20DtbCMsoa5AYFkDGk7IvjquvddFxOCRldDnDJyZI7RXB_QEMwuCbtpaclQLYwgYPf7HNP6r1OhNbzx0YkRnaz66P7DnyZAXSaHdiApjQ9xryI1i_uFgPb_ZpIJtIyC-VGRoxNu0tkaI1JOBGNOoq3-VYQ831wMaMeRLoiI7optCC1txfNW3WcA62hytPb5i34R-oHJ_8IpKvC8Sl3-lfgEIBIFmwmDTQ.eKfPYr1wKQtrt0n-Jt44DQ; awfs=s%3A4fugCSuqBOBXqgLf-i63fiVm4FvK-ssq.qFR7uvuUgSZ5Ql2MoDrouR9KKo4fxTt%2Bvy%2FHWjGjSQA; ASLBSA=0003025e6d959e0a2a34e16cf9b959447311f2c797d7e1e80dea30e306b1e1884f2eb00ed5e6774f8b2c2be7a88bbd516f1415d3a4c1477b301b724d3dbfcd8b4f2b; ASLBSACORS=0003025e6d959e0a2a34e16cf9b959447311f2c797d7e1e80dea30e306b1e1884f2eb00ed5e6774f8b2c2be7a88bbd516f1415d3a4c1477b301b724d3dbfcd8b4f2b'
    #COOKIE = r'rat=eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiemlwIjoiREVGIn0..NUFAeVF6_ZdwnYetmBC1lQ.XfPWCGh6aJgCZx_XjzLPXSJ0DKj3-kftyHeVWSlrgN6cdSzm9nxbGCc75Ejlsbpxe-XLRLWAfhTaMrdao0RJ-7IKlOGb45NP9Y3eu-6euCTSh3zq1PsFXiEdtUflrqYjz09zveiYdgzJpaHR5S7i6M_AM6RHSh2Jyg7vgJKzmdBSZs891Q99Yjf7Y11dGfatyi7wgv46nuRcZ9EDP6lfEvEfHe9KMNznHyYXv8BYddBOAns5-CRCvX5cBjhqk3ZQ5xdS5qepAjViPsrvvFz0Xe1uoA6kO-dFKkEnUSka5KB3pJ1J3N3b-4L5NpHtTyVI7HvxSW5VnGT4UB6IHpYp4ENn7Kv6OS4-YQ4L5bdb0oSBCgGTdhq3z60e48cHjPPw4RuZQTZXohNb9wv9zCtLhUgVAsAkw5ZJMYcqHmkoQqagTYvE6nlTZcGAf9XueA5Osw_oL4eYzk9xdypV8wdngw.AVzQQQdEmTcux6dmwis7Lg; awfs=s%3AX9a1aWBd1VRSgYJFBC_8JLSDKcVtnHKX.VZJkwnOar6I4g%2FMw0F8Cf39glWFiFt%2BJVZDb1P9Se9E; MSCC=NR; ARRAffinity=65412aadd2cc154dd3e6fbdb2ca0cd3268f789edf595355559949fb0202f1d23; ARRAffinitySameSite=65412aadd2cc154dd3e6fbdb2ca0cd3268f789edf595355559949fb0202f1d23; ASLBSA=0003025e6d959e0a2a34e16cf9b959447311f2c797d7e1e80dea30e306b1e1884f2e; ASLBSACORS=0003025e6d959e0a2a34e16cf9b959447311f2c797d7e1e80dea30e306b1e1884f2e'
    #REFERER = r'https://www.seaofthieves.com/profile/captaincy/your-ships/664e645e-35c6-4bc9-82b3-6fe9798645ca/3ed553c7-54bc-42e7-bf0a-78e360f3125c/14ccf7e2-b6cf-4d83-9ea5-51c9770d19f5:e321ed3e-7897-4147-a5b9-83687f4bc3ee:0'

    sotLoginCredentials: UserInformation.SotLoginCredentials = UserInformation.SotLoginCredentials(' '.join(args.msCookie))
    sotAnalyzerDetails: UserInformation.SotAnalyzerDetails = UserInformation.SotAnalyzerDetails(args.ship)
    userInfo = UserInformation.UserInformation(sotLoginCredentials, sotAnalyzerDetails, args.address)
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

    await ctx.send_msgs([
        {
            "cmd": "Connect",
            "game": "Sea of Thieves",
            "password": "",
            "name": "EthanSotReal",
            "uuid": "234234234",
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
    user_info.address = "192.168.0.210:38281"
    ctx = SOT_Context(user_info.address, None, user_info)
    await ctx.connect(user_info.address)


   # await fConnectToRoom(ctx)
    #p2 = multiprocessing.Process(target=)
   # while(1):
    #    time.sleep(1)
    #    print("hi")

    ctx.run_cli()
    #progression_watcher = asyncio.create_task(game_watcher(ctx), name="FactorioProgressionWatcher")
    f = asyncio.create_task(watchGameForever(ctx), name="ever")

    await ctx.exit_event.wait()
    #await progression_watcher
    await f
    await ctx.shutdown()
    return
    #
    # return
    # await fConnectToRoom(ctx)
    #
    # await cp.ctx.shutdown()
    # return
    #
    # a = asyncio.get_event_loop()
    #
    # # todo not sure what this every 3 does, but it seems to work for looping infinitly
    # #asyncio.run(main())
    # connectToRoom = ConnectToRoom(ctx)
    # connectToRoom.start()
    # getUpdatesAndSendItems = GetUpdatesAndSendItmes(ctx)
    # getUpdatesAndSendItems.start()
    # t1 = threading.Thread(target=ConnectToRoom, args=(cp.ctx,))
    # cp.ctx.run_cli()
    # await cp.ctx.exit_event.wait()
    # connectToRoom.join()
    # getUpdatesAndSendItems.join()
    # await cp.ctx.shutdown()
    # await cp.ctx.connect(user_info.address)
    #
    #
    # #print(msg)
    #
    # return
    #
    # #await ctx.send_msgs([{"cmd": "Connected", "slot":1}])
    # #await ctx.send_msgs([{"cmd": "Get", "keys": ["slot_data_1"]}])
    # if ctx.server_task is None:
    #     ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")




    #ctx.analyzer.setLocationsToRead(ctx.server_locations.copy())

    # if gui_enabled:
    #     pass
    # ctx.run_cli()
    #
    # await ctx.exit_event.wait()
    #
    # await ctx.shutdown()
    #
    # while (1):
    #
    #     #check every 5 seconds
    #     time.sleep(5)
    #     getUpdatesBasedOnItemsReceived(ctx)
    #     sendUpdatesBasedOnItemsFound(ctx)


if __name__ == '__main__':
    asyncio.run(main())

