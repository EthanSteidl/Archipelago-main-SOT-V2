from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.Name import Name
from ...Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items

class SettingsTreasuresSold:

    def __init__(self, allowSimple=1, allowRare=0):
        self.allowSimple = allowSimple
        self.allowRare = allowRare



class TreasuresSold(LocationsBase):

    L_GS_SELL_ANY = "Sell Anything"
    L_GS_SELL_CHEST = "Sell Chest"
    L_GS_SELL_SKULL = "Sell Skull"
    L_GS_SELL_DARK_RELIC = "Sell Dark Relic"
    L_GS_SELL_ARTIFACT = "Sell Artifact"
    L_GS_SELL_VAULT_KEY = "Sell Vault Key"
    L_GS_SELL_SIREN = "Sell Siren Gem"
    L_GS_SELL_MERMAID_GEM = "Sell Mermaid Gem"
    L_GS_SELL_BREATH_OF_THE_SEA = "Sell Breath of the Sea"
    L_GS_SELL_CHEST_ANIMAL_CRATE = "Sell Animal Crate"
    L_GS_SELL_CHEST_RESOURCE_CRATE = "Sell Resource Crate"
    L_GS_SELL_CHEST_TRADE_GOODS = "Sell Trade Goods"
    L_GS_SELL_CHEST_CARGO_GOODS = "Sell Cargo Goods"
    L_GS_SELL_FIREWORKS = "Sell Fireworks"
    L_GS_SELL_GIFTS = "Sell Reaper Gift"
    L_GS_SELL_EM_FLAG = "Sell Emissary Flag"
    L_GS_SELL_ASHEN_TOMB = "Sell Ashen Tomb"
    L_GS_SELL_REAPER_CHEST = "Sell Reaper's Chest"
    L_GS_SELL_BOX_OF_WONDERS = "Sell Box of Wondrous Secrets"


    def __init__(self):
        super().__init__()
        self.x = [0, 1, 1]
        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])

        web = WebItemJsonIdentifier(self.x[0], self.x[1], 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_ANY, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_CHEST, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_SKULL, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_DARK_RELIC, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_ARTIFACT, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_VAULT_KEY, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_SIREN, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 6)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_MERMAID_GEM, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 7)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_BREATH_OF_THE_SEA, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 8)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_CHEST_ANIMAL_CRATE, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 9)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_CHEST_RESOURCE_CRATE, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 10)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_CHEST_TRADE_GOODS, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 11)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_CHEST_CARGO_GOODS, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 12)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_FIREWORKS, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 13)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_GIFTS, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 14)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_EM_FLAG, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 15)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_ASHEN_TOMB, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 16)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_REAPER_CHEST, wlc))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 17)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_BOX_OF_WONDERS, wlc))

