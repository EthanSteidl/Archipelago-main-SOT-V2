import random

from .Hint import Hint
from BaseClasses import Location, Item, Region

def create_hint(itm: Item, rand: random.Random):
    return Hint(itm)