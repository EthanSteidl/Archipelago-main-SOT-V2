
from ..Configurations import SotOptionsDerived
from BaseClasses import MultiWorld, Region, Entrance, ItemClassification
from .Items import Items, ItemCollection, SOTItem
import math

def create_items(world: MultiWorld, location_count: int, options: SotOptionsDerived, itemCollection: ItemCollection, player: int):

    update_items_from_options(options, itemCollection)

    #region_adder = RegionAdder(player, locationDetailsCollection, options)

    # Check if we can place all the items
    item_count_to_add = itemCollection.getItemCount()
    filler_count_to_add = location_count - item_count_to_add
    if filler_count_to_add < 0:
        filler_count_to_add = 0


    # check if we can continue
    if item_count_to_add > location_count:
        raise Exception('Not enough locations to spawn items: {} Locations {} Items'.format(location_count, item_count_to_add))

    #trap count
    trap_count = int(math.floor(float(filler_count_to_add) * (float(options.trapsPercentage) / 100.0)))
    filler_count_to_add -= trap_count


    # Add main items
    for detail in itemCollection.progression:
        count_to_add_to_world = detail.countToSpawnByDefault - itemCollection.getPreFillCountForName(detail.name)
        if count_to_add_to_world < 0:
            count_to_add_to_world = 0
        for i in range(count_to_add_to_world):
            world.itempool.append(SOTItem(detail.name, detail.classification, detail.id, player))

    # Add filler items
    for i in range(filler_count_to_add):
        detail = world.random.choice(itemCollection.filler)
        world.itempool.append(SOTItem(detail.name, detail.classification, detail.id, player))

    # Add trap items
    for i in range(trap_count):
        detail = world.random.choice(itemCollection.trap)
        world.itempool.append(SOTItem(detail.name, detail.classification, detail.id, player))

def update_items_from_options(options: SotOptionsDerived, itemCollection: ItemCollection):
    itemCollection.informCollectionOfPrefillAction(Items.seal_gh.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.seal_ma.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.seal_af.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.seal_rb.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.seal_oos.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.pirate_legend.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.sail.name, 1)
