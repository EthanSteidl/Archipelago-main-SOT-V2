import typing

from worlds.seaofthieves.Client.Balance import Balance
class PlayerInventory:


    def __init__(self):

        #the idea here is to track how much money is made in SOT, how much fake money the client has, and how much total we have spent
        self.balanceSot = Balance(0, 0, 0)
        self.balanceClient = Balance(0, 0, 0)
        self.balanceSpent = Balance(0, 0, 0)
        self.owned_hints: typing.List[str] = []

        self.itemsToSendToClient = []

        self.item_names_in_inventory = {}

    def print_hints(self):
        for hint in self.owned_hints:
            print(hint)

    def add_hint(self, txt: str):
        self.owned_hints.append(txt)

    def add_item_to_client(self, id: int):
        self.itemsToSendToClient.append(id)

    def add_item(self, id: int):
        self.item_names_in_inventory[id] = True

    def setBalanceSot(self, bal: Balance):
        self.balanceSot = bal

    def addBalanceClient(self, bal: Balance):
        self.balanceClient = self.balanceClient + bal

    def getNominalBalance(self) -> Balance:
        return self.balanceSot + self.balanceClient - self.balanceSpent

    def canAfford(self, bal: Balance) -> bool:
        return not (self.getNominalBalance() - bal).isInDebt()

    def spend(self, bal: Balance) -> None:
        self.balanceSpent = self.balanceSpent + bal

    def add(self, bal: Balance) -> None:
        self.balanceSpent = self.balanceSpent - bal