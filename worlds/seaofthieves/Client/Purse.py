


class Purse:


    def __init__(self):
        self.gold = 0
        self.dabloons = 0
        pass

    def gainGold(self, v: int):
        self.gold += v

    def gainDabloons(self, v:int):
        self.dabloons += v

    def spendGold(self, v: int):
        self.gold -= v

    def spendDabloons(self, v: int):
        self.dabloons -= v

    def purseString(self) -> str:
        return r'Gold: {} Dabloons: {}'.format(self.gold, self.dabloons)