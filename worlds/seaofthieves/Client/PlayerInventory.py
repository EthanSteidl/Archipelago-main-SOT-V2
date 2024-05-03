from Purse import Purse


class PlayerInventory:


    def __init__(self):
        self.purse = Purse()

    def purseString(self) -> str:
        return self.purse.purseString()

    def add(self, gold: int, dabloons: int):
        self.purse.gainGold(gold)
        self.purse.gainDabloons(dabloons)

    def subtract(self, gold: int, dabloons: int):
        self.purse.spendGold(gold)
        self.purse.spendDabloons(dabloons)

    def has(self, gold: int, dabloons: int) -> bool:
        return self.purse.gold >= gold and self.purse.dabloons >= dabloons