from __future__ import annotations
# CommonClient import first to trigger ModuleUpdater
import json
import multiprocessing
import winsound
from worlds.seaofthieves.Locations.Locations import WebLocation
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
from worlds.seaofthieves.Items.Items import ItemCollection
from worlds.seaofthieves.Items.Items import Items, ItemDetail
from worlds.seaofthieves.Client.Shop import Shop,CombatShop
from worlds.seaofthieves.Configurations.SotOptionsDerived import SotOptionsDerived
import worlds.seaofthieves.Client.PlayerInventory as PlayerInventory
import pickle
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
import worlds.seaofthieves.Client.SOTDataAnalyzer as SOTDataAnalyzer
import typing
from NetUtils import ClientStatus, NetworkItem, JSONtoTextParser, JSONMessagePart, add_json_item, add_json_location, add_json_text, JSONTypes
import worlds.seaofthieves.Client.UserInformation as UserInformation
import argparse
import time
import asyncio
import multiprocessing
import logging
import Utils
from typing import NamedTuple
from worlds.seaofthieves.Client.NetworkProtocol.PrintJsonPacket import PrintJsonPacket
from worlds.seaofthieves.Client.NetworkProtocol.ReceivedItemsPacket import ReceivedItemsPacket
from worlds.seaofthieves.Client.NetworkProtocol.SetReply import SetReplyPacket
import worlds.seaofthieves.Client.Balance as Balance
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
                await ctx.init_notif_weapons()
                ctx.itemDets = ctx.itemCollection.getDictDetail()
                firstpass = False
            else:
                try:
                    ctx.updateSotPlayerBalance()
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

    def _cmd_forceunlock(self) -> bool:
        self.output("All location restrictions removed, tracking all. (Activates in 10 seconds)")
        self.ctx.forceUnlock = True

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

    def _cmd_locs(self):
        loc_details_possible: typing.List[LocDetails] = self.ctx.locationsReachableWithCurrentItems()
        print("You can check " + str(len(loc_details_possible)) + " more locations. ")
        for loc in loc_details_possible:
            print(loc.name)

    def _cmd_cshop(self):
        self.ctx.combatShop.info(self.ctx.playerInventory)
        return True

    def _cmd_cbuy(self, menu_line_number):
        menu_line_number = str(menu_line_number)
        detail: ItemDetail | None = self.ctx.combatShop.executeAction(menu_line_number, self.ctx.playerInventory)
        if detail is None:
            return

        asyncio.ensure_future(self.ctx.set(detail.name, 1))


    def _cmd_mrkrabs(self):
        print("You now have alot of money.")
        self.ctx.playerInventory.addBalanceClient(Balance.Balance(100000000,100000000,10000000))



class SOT_Context(CommonContext):
    command_processor = SOT_CommandProcessor


    def __init__(self, serverAddress: str | None, serverPassword: str | None, userInformation: UserInformation.UserInformation):
        super().__init__(serverAddress, serverPassword)
        self.userInformation = userInformation
        self.analyzer: SOTDataAnalyzer.SOTDataAnalyzer = SOTDataAnalyzer.SOTDataAnalyzer(userInformation)
        self.known_items_received = [] #used to track measured received counts

        self.locationDetailsCollection = LocationDetailsCollection()
        self.discoveryHints = {}

        self.itemCollection = ItemCollection()
        self.itemDets: typing.Dict[str, ItemDetail] = {}
        self.shop = Shop()
        self.combatShop = CombatShop()
        self.playerInventory = PlayerInventory.PlayerInventory()
        self.connected_to_server = False

        self.originalBalance: Balance.Balance | None = None

        self.options: SotOptionsDerived = SotOptionsDerived()

        self.forceUnlock = False


    async def init_notif_weapons(self):
        keys: typing.List[str] = []
        if len(ItemCollection.combat) <= 0:
            return
        for det in ItemCollection.combat:
            keys.append(str(det.name))

            await self.send_msgs([
                {
                    "cmd": "SetNotify",
                    "keys": keys,
                }
            ])
        return

    def locationsReachableWithCurrentItems(self, forceUnlock: bool = False) -> typing.List[LocDetails]:

        returnList: typing.Set[str] = set()
        currentItems: typing.Set[str] = set()

        # check out our current items
        for item in self.items_received:
            id = item.item
            name: str = self.itemCollection.getNameFromId(id)

            #if the name is null, there is a bug but we should handle it here
            if(name != ""):
                currentItems.add(name)


        return self.locationDetailsCollection.findDetailsCheckable(currentItems, forceUnlock)


    def on_package(self, cmd: str, args: dict):
        if cmd == "RoomInfo":
            asyncio.create_task(fConnectToRoom(self), name="FConnecToRoom")

        elif cmd == "Connected":
            self.connected_to_server = True
            self.discoveryHints = args["slot_data"]
            self.shop.set_hints_generic(self.discoveryHints['HINTS_GENERAL'])
            self.shop.set_hints_personal_progression(self.discoveryHints['HINTS_PERSONAL_PROG'])
            self.shop.set_hints_other_progression(self.discoveryHints['HINTS_OTHER_PROG'])

            self.locationDetailsCollection.applyOptions(self.options)
            self.locationDetailsCollection.addAll()
            print(args)

        elif cmd == "LocationInfo":
            pass
            # TODO we should acknowledge the items have been recieved and stop sending them again

        elif cmd == "RoomUpdate":
            pass

        elif cmd == "Bounced":
            pass

        elif cmd == "Retrieved":
            pass

        elif cmd == "ReceivedItems":


            receivedItemsPacket: ReceivedItemsPacket = ReceivedItemsPacket(args)
            if(receivedItemsPacket.items is not None):
                self.items_received = receivedItemsPacket.items



        elif cmd == "PrintJSON":
            printJsonPacket: PrintJsonPacket = PrintJsonPacket(args)
            printJsonPacket.print()

        elif cmd == "SetReply":
            setReplyPacket: SetReplyPacket = SetReplyPacket(args)
            if(setReplyPacket.value != 0 and setReplyPacket.original_value == 0):
                self.playAudio(setReplyPacket.key)

        else:
            print("Error: Server requested unsupported feature '{0}'".format(cmd))

            #this is where you read slot data if any

    def playAudio(self, key: str):
        if key in self.itemDets.keys() and self.itemDets[key].sound_file != "":
            fpath = '..\\Items\\Sounds\\' + self.itemDets[key].sound_file
            winsound.PlaySound(fpath, winsound.SND_FILENAME)
        return
    def applyMoneyIfMoney(self, itm: NetworkItem):
        gold_ids: typing.Dict[int, int] = {Items.Filler.gold_50.id: Items.Filler.gold_50.numeric_value,
                    Items.Filler.gold_100.id: Items.Filler.gold_100.numeric_value,
                    Items.Filler.gold_500.id: Items.Filler.gold_500.numeric_value}
        id = itm.item
        if id in gold_ids.keys():
            gold_val = gold_ids[id]
            ac = 0
            db = 0
            self.playerInventory.addBalanceClient(Balance.Balance(ac, db, gold_val))

        return

    def acknowledgeItemsReceived(self):
        for itm in self.items_received:
            if(itm not in self.known_items_received):
                self.applyMoneyIfMoney(itm)
        self.known_items_received = self.items_received

    def getAndClearNewLocationsReached(self) -> typing.Set[int]:
        locations: typing.Set[int] = set()
        checks = self.analyzer.getAllChecks()
        for locId, isChecked in checks.items():
            if(isChecked):
                locations.add(locId)

        return locations

    def updateAnalyzerWithLocationsPossible(self):

        loc_details_possible: typing.List[LocDetails] = self.locationsReachableWithCurrentItems(self.forceUnlock)
        for loc_detail in loc_details_possible:
            self.analyzer.allowTrackingOfLocation(loc_detail)
        self.acknowledgeItemsReceived()


    def updateSotPlayerBalance(self):
        newBalance = self.analyzer.getBalance()

        if self.originalBalance is None:
            self.originalBalance = newBalance

        newBalance = newBalance - self.originalBalance
        self.playerInventory.setBalanceSot(newBalance)


    async def set(self, key, value):
        # Sync server itmes to us
        await self.send_msgs([
            {
                "cmd": "Set",
                "key": key,
                "default": 0,
                "want_reply": 1,
                "operations": [{"operation": "replace", "value": value}]
            }
        ])
    async def collectLocationsAndSendInformation(self):

        # Sync server itmes to us
        await self.send_msgs([
            {
                "cmd": "Sync"
            }
        ])

        # Use those items to check if we can finish anything
        self.analyzer.update()
        completedChecks: typing.Dict[int, bool] = self.analyzer.getAllCompletedChecks()
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
    parser.add_argument('--options', dest='options', type=str,
                        help='Options YAML file', nargs='+')
    args = parser.parse_args()
    if args.msCookie is not None:
        filepath = args.msCookie[0]
        while not os.path.exists(filepath):
            filepath = input('File not found. Enter an absolute Filepath to a text file containing your mscookie : ')
        file = open(filepath, "r")
        args.msCookie
        real_cookie = str(file.read())
        file.close()
    if( args.address is None or args.ship is None or args.msCookie is None or args.username is None):
        print("Error: Expected command line arguments")
        print("Required \"--address <ipaddress:port>\"")
        print("Required \"--ship <shipNumber>\"")
        print("Required \"--mscookie <cookie>\"")
        print("Required \"--user <username>\"")
        print("Example Command: python SotCustomClient.py --address 127.0.0.1:25255 --ship 1 --mscookie 1j23iuo1j23p1h2j3p1h")

        print("\nEnter missing arguments now.")
        if(args.address is None):
            args.address = input('Enter address:port : ')
        if (args.ship is None):
            args.ship = input('Enter ship Number : ')
        if (args.msCookie is None):
            filepath = input('Enter an absolute Filepath to a text file containing your mscookie : ')
            while not os.path.exists(filepath):
                filepath = input('File not found. Enter an absolute Filepath to a text file containing your mscookie : ')
            file = open(filepath, "r")
            real_cookie = str(file.read())
            file.close()
        if (args.username is None):
            args.username = input('Enter user : ')


    if args.options is not None:
        filepath = args.options[0]
        while not os.path.exists(filepath):
            filepath = input('File not found. Enter an absolute Filepath to a text file containing your options.yaml : ')
        file = open(filepath, "rb")
        options = pickle.load(file)
        file.close()
    else:
        print("Missing options argument")
        exit(1)

    sotLoginCredentials: UserInformation.SotLoginCredentials = UserInformation.SotLoginCredentials(real_cookie)
    sotAnalyzerDetails: UserInformation.SotAnalyzerDetails = UserInformation.SotAnalyzerDetails(args.ship, None)
    userInfo = UserInformation.UserInformation(sotLoginCredentials, sotAnalyzerDetails, args.address, args.username, options)
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

