import random

from .Hint import Hint
from BaseClasses import Location, Item, Region


def hint_from_item(itm: Item) -> Hint:
    return Hint(itm)


def hint_from_location(loc: Location) -> Hint:
    return Hint(loc.item)
