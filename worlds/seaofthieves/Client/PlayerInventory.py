

from worlds.seaofthieves.Client.Balance import Balance
class PlayerInventory:


    def __init__(self):

        #the idea here is to track how much money is made in SOT, how much fake money the client has, and how much total we have spent
        self.balanceSot = Balance(0,0,0)
        self.balanceClient = Balance(0,0,0)
        self.balanceSpent = Balance(0,0,0)

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