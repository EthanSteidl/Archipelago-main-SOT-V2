from __future__ import annotations

import random
import time

# CommonClient import first to trigger ModuleUpdater
import winsound
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
from worlds.seaofthieves.Items.Items import ItemCollection
from worlds.seaofthieves.Items.Items import Items, ItemDetail
from worlds.seaofthieves.Client.Shop import Shop
from worlds.seaofthieves.Configurations.SotOptionsDerived import SotOptionsDerived
from worlds.seaofthieves import ClientInput
import worlds.seaofthieves.Client.PlayerInventory as PlayerInventory
import colorama
import os
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser
import threading
import worlds.seaofthieves.Client.SOTDataAnalyzer as SOTDataAnalyzer
import typing
from NetUtils import ClientStatus, NetworkItem, JSONtoTextParser, JSONMessagePart, add_json_item, add_json_location, add_json_text, JSONTypes
import worlds.seaofthieves.Client.UserInformation as UserInformation
import argparse
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
    first_pass = True
    while True:

        if ctx.connected_to_server:
            if first_pass:
                await ctx.init_notif()
                first_pass = False
            else:
                try:
                    ctx.updateSotPlayerBalance()
                    ctx.updateAnalyzerWithLocationsPossible()
                    await ctx.collectLocationsAndSendInformation()
                except Exception as e:
                    print("Fatal error occurred: ", e)

        await asyncio.sleep(1)

class SOT_CommandProcessor(ClientCommandProcessor):
    ctx: SOT_Context

    def _cmd_hints(self) -> bool:
        """Displays hints you have purchased"""
        self.ctx.playerInventory.print_hints()
        return True

    def _cmd_forceunlock(self) -> bool:
        """Removes all location logic restrictions"""
        self.output("All location restrictions removed, tracking all. (Activates in 10 seconds)")
        self.ctx.forceUnlock = True


    def _cmd_linkShip(self, command: str) -> bool:
        """Tracks another ship on this world"""
        print("Not Implemented")
        return False

        # #command in form "shipName<->mscookie"
        # args = command.split("<->")
        # if len(args) < 2:
        #     print("Invalid argument count of " + str(len(args)) + ". Expected 2.")
        #     return False
        #
        # shipName = args[0]
        # msCookie = args[1]
        # #self.ctx.analyzer.addShip(shipName, msCookie)
        # return True
    def _cmd_linkPirate(self, command: str) -> bool:
        """Tracks another pirate on this world"""
        print("Not Implemented")
        return False

        # #command in form "shipName<->mscookie"
        # args = command.split("<->")
        # if len(args) < 2:
        #     print("Invalid argument count of " + str(len(args)) + ". Expected 2.")
        #     return False
        #
        # name = args[0]
        # msCookie = args[1]
        # #self.ctx.analyzer.addPirate(name, msCookie)
        # return True

    def _cmd_shop(self) -> bool:
        """Opens the shop"""
        self.ctx.shop.info(self.ctx.playerInventory)
        return True

    def _cmd_buy(self, menu_line_number):
        """Allows you to buy an item from the shop"""
        menu_line_number = str(menu_line_number)
        self.ctx.shop.executeAction(menu_line_number, self.ctx.playerInventory)

    def _cmd_locs(self):
        """Displays locations you can currently complete"""
        loc_details_possible: typing.List[LocDetails] = self.ctx.locationsReachableWithCurrentItems()


        checked = len(self.ctx.locations_checked)
        possible = 0

        for loc in loc_details_possible:
            if loc.id not in self.ctx.locations_checked and loc.doRandomize:
                possible += 1
        print("You can check " + str(possible) + " more locations. And have completed " + str(checked))
        for loc in loc_details_possible:
            if loc.id not in self.ctx.locations_checked and loc.doRandomize:
                print(loc.name)

    def _cmd_complete(self, locId):
        """Force completes a check"""
        self.ctx.locations_checked.add(int(locId))
        self.ctx.analyzer.stopTracking(int(locId))


    def _cmd_mrkrabs(self):
        """Gives you alot of money"""
        print("You now have alot of money.")
        self.ctx.playerInventory.addBalanceClient(Balance.Balance(100000000,100000000,10000000))



class SOT_Context(CommonContext):
    command_processor = SOT_CommandProcessor


    def __init__(self, serverAddress: typing.Optional[str], serverPassword: str | None, userInformation: UserInformation.UserInformation):
        super().__init__(serverAddress, serverPassword)
        self.userInformation = userInformation
        self.analyzer: SOTDataAnalyzer.SOTDataAnalyzer = SOTDataAnalyzer.SOTDataAnalyzer(userInformation)
        self.known_items_received = [] #used to track measured received counts

        self.locationDetailsCollection = LocationDetailsCollection()
        self.discoveryHints = {}

        self.itemCollection = ItemCollection()
        self.shop = Shop()
        self.playerInventory = PlayerInventory.PlayerInventory()
        self.connected_to_server = False

        self.originalBalance: Balance.Balance | None = None

        self.options: SotOptionsDerived = userInformation.options
        self.region_connection_details = userInformation.regionLogic

        self.forceUnlock = False



        self.balance_update_interval = 10
        self.balance_last_update = -10000


    async def init_notif(self):
        keys: typing.List[str] = []

        keys.append(Items.golden_dragon.name)

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
            self.locationDetailsCollection.applyRegionDiver(self.region_connection_details)
            self.locations_checked = set(args["checked_locations"])


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
            if setReplyPacket.key is Items.golden_dragon.name:
                puns = [
                    "Captain! " + colorama.Fore.YELLOW + "Another Player " + colorama.Fore.RESET + "leveraged to much naval real estate and succumbed to collections",
                    "Captain! " + colorama.Fore.YELLOW + "Another Player " + colorama.Fore.RESET + "invested their money in an MLM",
                    "Captain! " + colorama.Fore.YELLOW + "Another Player " + colorama.Fore.RESET + "sent their money to a long lost royal relative stuck in prison"
                ]

                print(random.choice(puns))

            self.playAudio(setReplyPacket.key)

        else:
            print("Error: Server requested unsupported feature '{0}'".format(cmd))

            #this is where you read slot data if any

    def playAudio(self, key: str):
        if not self.options.experimentals:
            return
        return
    def applyMoneyIfMoney(self, itm: NetworkItem):

        gold_ids: typing.Dict[int, int] = {Items.gold_50.id: Items.gold_50.numeric_value,
                    Items.gold_100.id: Items.gold_100.numeric_value,
                    Items.gold_500.id: Items.gold_500.numeric_value}

        dabloon_ids: typing.Dict[int, int] = {Items.dabloons_25.id: Items.dabloons_25.numeric_value}

        coin_ids: typing.Dict[int, int] = {Items.ancient_coins_10.id: Items.ancient_coins_10.numeric_value}
        id = itm.item
        if id in gold_ids.keys():
            gold_val = gold_ids[id]
            ac = 0
            db = 0
            self.playerInventory.addBalanceClient(Balance.Balance(ac, db, gold_val))

        elif id == Items.golden_dragon:
            print("Captain! The legendary " + colorama.Fore.YELLOW + Items.golden_dragon.name + colorama.Style.RESET_ALL + " is comming for your " + colorama.Fore.GREEN + "COINS" + colorama.Fore.RESET + ". You are now broke.")
            self.playerInventory.setBalanceSot(Balance.Balance(-10000, -10000, -10000))
            self.add(Items.golden_dragon.name)

        elif id in dabloon_ids.keys():
            gold_val = 0
            ac = 0
            db = dabloon_ids[id]
            self.playerInventory.addBalanceClient(Balance.Balance(ac, db, gold_val))

        elif id in coin_ids.keys():
            gold_val = 0
            ac = coin_ids[id]
            db = 0
            self.playerInventory.addBalanceClient(Balance.Balance(ac, db, gold_val))

        return

    def acknowledgeItemsReceived(self):
        should_play_sound = False
        for itm in self.items_received:
            if(itm not in self.known_items_received):
                should_play_sound = True

        if should_play_sound and self.options.experimentals:
            fpath = '..\\Items\\Sounds\\item_find.wav'
            winsound.PlaySound(fpath, winsound.SND_FILENAME)
        self.known_items_received = self.items_received


    def updateAnalyzerWithLocationsPossible(self):

        loc_details_possible: typing.List[LocDetails] = self.locationsReachableWithCurrentItems(self.forceUnlock)
        for loc_detail in loc_details_possible:
            self.analyzer.allowTrackingOfLocation(loc_detail)
        self.acknowledgeItemsReceived()


    def updateSotPlayerBalance(self):

        #Optimizing compute time to spend more time on screen recognition
        if self.balance_last_update + self.balance_update_interval > time.time():
            return

        newBalance = self.analyzer.getBalance()

        if self.originalBalance is None:
            self.originalBalance = newBalance

        newBalance = newBalance - self.originalBalance
        self.playerInventory.setBalanceSot(newBalance)

    async def add(self, key):
        # Sync server itmes to us
        await self.send_msgs([
            {
                "cmd": "Set",
                "key": key,
                "default": 0,
                "want_reply": 1,
                "operations": [{"operation": "add", "value": 1}]
            }
        ])

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
    parser.add_argument('--clientInput', dest='clientInput', type=str,
                        help='Client Input File', nargs='+')
    args = parser.parse_args()
    if args.msCookie is not None:
        filepath = args.msCookie[0]
        while not os.path.exists(filepath):
            filepath = input('File not found. Enter an absolute Filepath to a text file containing your mscookie : ')
        file = open(filepath, "r")
        real_cookie = str(file.read())
        if real_cookie == "":
            print("Your file is empty, ERROR")
            exit(1)
        if real_cookie[0] == "\n":
            print("Warning: Your file contains a newline at the start file. Confirm this is correct")
        file.close()

    if args.clientInput is not None:
        filepath = args.clientInput[0]
        while not os.path.exists(filepath):
            filepath = input(
                'File not found. Enter an absolute Filepath to a text file containing your client input: ')
        clientInput: ClientInput = ClientInput()
        clientInput.from_fire(filepath)



    if( args.address is None or args.ship is None or args.msCookie is None or args.clientInput is None or args.clientInput is None):
        print("Error: Expected command line arguments")
        print("Required \"--address <ipaddress:port>\"")
        print("Required \"--ship <shipNumber>\"")
        print("Required \"--mscookie <cookie>\"")
        print("Example Command: python SotCustomClient.py --address 127.0.0.1:25255 --ship 1 --mscookie 1j23iuo1j23p1h2j3p1h")

        print("\nEnter missing arguments now.")
        if(args.address is None):
            args.address = input('Enter address:port : ')
        if (args.ship is None):
            args.ship = input('Enter ship Number or "NA" for pirate mode: ')
        if (args.msCookie is None):
            filepath = input('Enter an absolute Filepath to a text file containing your mscookie : ')
            while not os.path.exists(filepath):
                filepath = input('File not found. Enter an absolute Filepath to a text file containing your mscookie : ')
            file = open(filepath, "r")
            real_cookie = str(file.read())
            file.close()
        if (args.clientInput is None):
            filepath = input('Enter an absolute Filepath to a text file containing your options : ')
            while not os.path.exists(filepath):
                filepath = input(
                    'File not found. Enter an absolute Filepath to a text file containing your options : ')
            clientInput: ClientInput = ClientInput()
            clientInput.from_fire(filepath)


    pirate = None
    if args.ship == "NA":
        args.ship = None
        pirate = "pirateMode"
    sotLoginCredentials: UserInformation.SotLoginCredentials = UserInformation.SotLoginCredentials(real_cookie)
    sotAnalyzerDetails: UserInformation.SotAnalyzerDetails = UserInformation.SotAnalyzerDetails(args.ship, pirate)
    userInfo = UserInformation.UserInformation(sotLoginCredentials, sotAnalyzerDetails, args.address, clientInput)
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


async def main():
    Utils.init_logging("Sea of Thieves")
    multiprocessing.freeze_support()
    user_info: UserInformation.UserInformation = getSeaOfThievesDataFromArguments()
    ctx = SOT_Context(user_info.address, None, user_info)

    await ctx.connect(user_info.address)

    ctx.run_cli()
    game_watcher = asyncio.create_task(watchGameForever(ctx), name="ever")

    await ctx.exit_event.wait()
    await game_watcher
    await ctx.shutdown()

    return

def launch():
    asyncio.run(main())

if __name__ == '__main__':
    asyncio.run(main())

