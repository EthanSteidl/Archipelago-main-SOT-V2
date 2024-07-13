
from ..Locations import LocDetails, SOTLocation
from .Balance import Balance

class ShopLocation(SOTLocation):

    def __init__(self, locDetails: LocDetails, player: int, region, price: Balance):
        super().__init__(locDetails, player, region)

        self.price: Balance = price


    def display_text(self) -> str:
        return "{}: {}".format(self.item.name, self.price.displayString())