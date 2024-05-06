from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier, DoRand
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.Name import Name
from ...Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items

class SettingsSeals:

    def __init__(self, gh_amt=10000, ma_amt=10000, oos_amt=10000, af_amt=10000, rb_amt=10000):
        self.gh_amt = gh_amt
        self.ma_amt = ma_amt
        self.oos_amt = oos_amt
        self.af_amt = af_amt
        self.rb_amt = rb_amt

    def getSettingForLocName(self, name: str):
        if (name == Seals.L_SEAL_AF):
            return self.gh_amt
        if (name == Seals.L_SEAL_RB):
            return self.ma_amt
        if (name == Seals.L_SEAL_GH):
            return self.oos_amt
        if (name == Seals.L_SEAL_MA):
            return self.af_amt
        if (name == Seals.L_SEAL_OOS):
            return self.rb_amt
        # default for it to be enabled
        return 10000


class Seals(LocationsBase):


    L_VOYAGE_COMP_GH_TOTAL = "Complete Voyage (GH)"
    L_VOYAGE_COMP_MA_TOTAL = "Complete Voyage (MA)"
    L_VOYAGE_COMP_OOS_TOTAL = "Complete Voyage (OOS)"
    L_VOYAGE_COMP_AF_TOTAL = "Complete Voyage (AF)"
    L_VOYAGE_COMP_RB_TOTAL = "Complete Voyage (RB)"



    def __init__(self):
        super().__init__()
        self.x = [2, 0, 0, -1]

        reg = RegionNameCollection()
        reg.addFromList([Name.DOMAIN_GH])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.voyages_gh])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(1, 1, 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_GH_TOTAL, wlc, True))

        reg = RegionNameCollection()
        reg.addFromList([Name.DOMAIN_MA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.voyages_ma])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(1, 2, 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_MA_TOTAL, wlc, True))

        reg = RegionNameCollection()
        reg.addFromList([Name.DOMAIN_OOS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.voyages_oos])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(1, 3, 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_OOS_TOTAL, wlc, True))

        reg = RegionNameCollection()
        reg.addFromList([Name.DOMAIN_AF])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.voyages_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(1, 4, 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF_TOTAL, wlc, True))

        #RB is to sell a reaper chest/bounty?
        reg = RegionNameCollection()
        reg.addFromList([Name.DOMAIN_RB])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.voyages_rb])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(0, 6, 1, 0), reg, lgc),
            WebLocation(WebItemJsonIdentifier(0, 6, 1, 1), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_RB_TOTAL, wlc, True))


