import json

class Balance:

    def __init__(self, ancientCoins: int = 0, dabloons: int = 0, gold: int = 0):
        self.ancientCoins = ancientCoins
        self.dabloons = dabloons
        self.gold = gold
        self.imageUrl = ""

    def __sub__(self, other):
        self.ancientCoins -= other.ancientCoins
        self.dabloons -= other.dabloons
        self.gold -= other.gold
        return self

    def __add__(self, other):
        self.ancientCoins += other.ancientCoins
        self.dabloons += other.dabloons
        self.gold += other.gold
        return self

    def isInDebt(self) -> bool:
        if self.ancientCoins < 0 or self.dabloons < 0 or self.gold < 0:
            return True
        return False

    def displayString(self) -> str:
        return "Gold: {} Dabloons: {} AncientCoins: {}".format(self.gold, self.dabloons, self.ancientCoins)

def fromJson(js: json) -> Balance:
    return Balance(js["ancientCoins"], js["doubloons"], js["gold"])