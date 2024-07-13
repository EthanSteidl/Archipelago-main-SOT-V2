import typing
from .ShopLocation import ShopLocation
from ..Locations import LocDetails


class ShopLocationList():

    def __init__(self, name: str, shop_locations: typing.Optional[typing.List[ShopLocation]] = None):
        self.name: str = name
        self.shop_locations: typing.List[ShopLocation] = list() if shop_locations is None else shop_locations

    def add(self, loc_det: LocDetails):
        return
        #shopLocation: ShopLocation = ShopLocation(loc_det, )
        #self.shop_locations.append(loc)

    def display_text(self) -> str:
        txt: str = ""
        line: int = 1
        for loc in self.shop_locations:
            txt += "[{}] {}\n".format(line, loc.display_text())
        return txt

