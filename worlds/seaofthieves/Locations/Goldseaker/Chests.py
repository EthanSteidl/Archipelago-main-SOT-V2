import copy

from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier, DoRand
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.Name import Name
from ...Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items

class SettingsChest:

    def __init__(self, gh_count=10, ma_count=10, oos_count=10, rb_count=2, af_count=5):
        self.gh_count = gh_count
        self.ma_count = ma_count
        self.oos_count = oos_count
        self.rb_count = rb_count
        self.af_count = af_count



class Chests(LocationsBase):

    L_UN_SELL_CHEST = "Sell (GH)"
    L_UN_SELL_SKULL = "Sell (OoS)"
    L_UN_SELL_MERCH = "Sell (MA)"
    L_UN_SELL_AF = "Sell (AF)"
    L_UN_SELL_RB = "Sell (RB)"


    def __init__(self, settings: SettingsChest):
        super().__init__()
        self.x = [0, 1, 1]
        reg = RegionNameCollection()
        reg.addFromList([Name.DOMAIN_GH])
        lgc = ItemReqEvalOr([])
        web = WebItemJsonIdentifier(0, 2, 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        for i in range(1, settings.gh_count+1):
            cnt = i*5
            self.locations.append(LocDetails(self.L_UN_SELL_CHEST + " " + str(cnt), copy.deepcopy(wlc)))
            itm_detail = copy.deepcopy(Items.upgrade_cnt_gh)
            itm_detail.req_qty = cnt
            lgc = ItemReqEvalOr([itm_detail])
            wlc = WebLocationCollection([WebLocation(web, reg, lgc)])



        reg = RegionNameCollection()
        reg.addFromList([Name.DOMAIN_OOS])
        lgc = ItemReqEvalOr([])
        web = WebItemJsonIdentifier(0, 4, 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(1, settings.oos_count+1):
            cnt = i * 5
            self.locations.append(LocDetails(self.L_UN_SELL_SKULL + " " + str(i), copy.deepcopy(wlc)))
            itm_detail = copy.deepcopy(Items.upgrade_cnt_gh)
            itm_detail.req_qty = cnt
            lgc = ItemReqEvalOr([itm_detail])
            wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        reg = RegionNameCollection()
        reg.addFromList([Name.DOMAIN_MA])
        lgc = ItemReqEvalOr([])
        web = WebItemJsonIdentifier(0, 3, 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(1, settings.ma_count+1):
            cnt = i * 5
            self.locations.append(LocDetails(self.L_UN_SELL_MERCH + " " + str(i), copy.deepcopy(wlc)))
            itm_detail = copy.deepcopy(Items.upgrade_cnt_ma)
            itm_detail.req_qty = cnt
            lgc = ItemReqEvalOr([itm_detail])
            wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        reg = RegionNameCollection()
        reg.addFromList([Name.DOMAIN_AF])
        lgc = ItemReqEvalOr([])
        web = WebItemJsonIdentifier(0, 5, 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(1, settings.af_count+1):
            cnt = i
            self.locations.append(LocDetails(self.L_UN_SELL_AF + " " + str(cnt), copy.deepcopy(wlc)))
            itm_detail = copy.deepcopy(Items.upgrade_cnt_af)
            itm_detail.req_qty = cnt
            lgc = ItemReqEvalOr([itm_detail])
            wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        reg = RegionNameCollection()
        reg.addFromList([Name.DOMAIN_RB])
        lgc = ItemReqEvalOr([])
        web = WebItemJsonIdentifier(0, 6, 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(1, settings.rb_count+1):
            cnt = i
            self.locations.append(LocDetails(self.L_UN_SELL_RB + " " + str(cnt), copy.deepcopy(wlc)))
            itm_detail = copy.deepcopy(Items.upgrade_cnt_rb)
            itm_detail.req_qty = cnt
            lgc = ItemReqEvalOr([itm_detail])
            wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

