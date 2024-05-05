from __future__ import annotations
# CommonClient import first to trigger ModuleUpdater
import json
import multiprocessing
import winsound
from worlds.seaofthieves.Locations.Locations import WebLocation
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
from worlds.seaofthieves.Items.Items import ItemCollection
from worlds.seaofthieves.Items.Items import Items, ItemDetail

from .Shop import Shop,CombatShop
import worlds.seaofthieves.Client.PlayerInventory as PlayerInventory
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
                firstpass = False
            else:
                try:
                    ctx.updateSotPlayerBalance()
                    print("1")
                    ctx.updateAnalyzerWithLocationsPossible()
                    print("2")
                    await ctx.collectLocationsAndSendInformation()
                    print("3")
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
        detail: ItemDetail = self.ctx.combatShop.executeAction(menu_line_number, self.ctx.playerInventory)
        self.ctx.set(detail.id, 1)

    def _cmd_mrkrabs(self):
        self.ctx.playerInventory.addBalanceClient(Balance.Balance(10000000,10000000,1000000))



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
        self.shop = Shop()
        self.combatShop = CombatShop()
        self.playerInventory = PlayerInventory.PlayerInventory()
        self.connected_to_server = False

        self.originalBalance: Balance.Balance | None = None


    async def init_notif_weapons(self):
        keys: typing.List[str] = []
        if len(ItemCollection.combat) <= 0:
            return
        for det in ItemCollection.combat:
            keys.append(str(det.id))

            await self.send_msgs([
                {
                    "cmd": "SetNotify",
                    "keys": keys,
                }
            ])
        return

    def locationsReachableWithCurrentItems(self) -> typing.List[LocDetails]:

        returnList: typing.Set[str] = set()
        currentItems: typing.Set[str] = set()

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
            self.discoveryHints = args["slot_data"]
            self.shop.set_hints_generic(self.discoveryHints['HINTS_GENERAL'])
            self.shop.set_hints_personal_progression(self.discoveryHints['HINTS_PERSONAL_PROG'])
            self.shop.set_hints_other_progression(self.discoveryHints['HINTS_OTHER_PROG'])
            print(args)

        elif cmd == "LocationInfo":
            pass
            # TODO we should acknowledge the items have been recieved and stop sending them again

        elif cmd == "RoomUpdate":
            pass
            #print("We got a room update")
            #print(args)

        elif cmd == "Bounced":
            #do nothing
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
        if(key == str(Items.Combat.c_tac_missle.id)):
            winsound.PlaySound('Sounds\\warning_fixed.wav', winsound.SND_FILENAME)
            winsound.PlaySound('Sounds\\tac_missle_fixed.wav', winsound.SND_FILENAME)
        if(key == str(Items.Combat.c_orbital_rail)):
            winsound.PlaySound('Sounds\\warning_fixed.wav', winsound.SND_FILENAME)
            winsound.PlaySound('Sounds\\orbital_rail_fixed.wav', winsound.SND_FILENAME)
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

            #TODO remove this 50
            gold_val += 50
            ac += 1
            db +=5
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

        loc_details_possible: typing.List[LocDetails] = self.locationsReachableWithCurrentItems()
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
    args = parser.parse_args()

    if( args.address is None or args.ship is None or args.msCookie is None or args.user is None):
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
            args.msCookie = file.read()
            file.close()
        if (args.username is None):
            args.username = input('Enter user : ')


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

