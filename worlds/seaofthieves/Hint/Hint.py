
from BaseClasses import Location, Item, Region
from .PhraseGroup import PhraseGroup
import random
class Hint:


    I_NAME_R_NAME = PhraseGroup(["The {} can be found within the {}."])
    I_NAME_L_NAME = PhraseGroup(["The {} can be found within the {}."])
    I_NAME_P_RECEIVE_R_NAME = PhraseGroup(["The {} for player {} can be found within the {}."])
    I_NAME_P_RECEIVE_L_NAME = PhraseGroup(["The {} for player {} can be found within the {}."])
    def __init__(self, item: Item):
        self.item = item
        self.counter = item.code + item.player # The idea is to add a bit of randomization, without needing to call rand
        pass

    def get(self, rand: random.Random):
        idx: int = rand.randint(0, 3)

        match idx:
            case 0:
                return Hint.I_NAME_R_NAME.getRandom().format(self.item.name, self.item.location.parent_region.name)
            case 1:
                return Hint.I_NAME_L_NAME.getRandom().format(self.item.name, self.item.location.name)
            case 2:
                return Hint.I_NAME_P_RECEIVE_R_NAME.getRandom().format(self.item.name, self.item.player ,self.item.location.parent_region.name)
            case 3:
                return Hint.I_NAME_P_RECEIVE_L_NAME.getRandom().format(self.item.name, self.item.player ,self.item.location.parent_region.name)
            case _:
                return Hint.I_NAME_R_NAME.getRandom().format(self.item.name, self.item.location.parent_region.name)