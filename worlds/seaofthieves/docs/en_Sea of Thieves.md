# Sea of Thieves

## What does randomization do to this game?

This is not a mod for sea of thieves and works by reading player stats from www.seaofthieves.com. This randomizer does not prevent you from performing checks in game that you should not have access to. However, the randomizer keeps track of what you should be able to do in your game and will not award items for loactions that you have yet to recieve the items to check.


The following are randomized as items:
1. Sail - Unlocks the ability to check locations away from the starting island
2. Inferno Sail - Unlocks the ability to check locations in the Devil's Roar
3. Voyages of Fortresses - Allows location rewards related to Fortresses
4. Voyages of Gold Hoarders - Allows location rewards for completing Voyages
5. Voyages of Merchants - Allows location rewards for completing  voyages
6. Voyages of Souls - Allows location rewards for completing voyages
7. Voyages of Athena - Allows location rewards for completing voyages
8. Voyages of Reaper - Allows location rewards for selling any Reaper chest
9. Emissary of Gold Hoarders - Allows location rewards for emmissary actions
10. Emissary of Merchants - Allows location rewards for emmissary actions
11. Emissary of Souls - Allows location rewards for emmissary actions
12. Emissary of Athena - Allows location rewards for emmissary actions
13. Emissary of Reaper - Allows location rewards for emmissary actions
14. Voyages of Destiny - Allows access to Fort of the Damned
15. Personal Weapons - Allows access to pirate combat related loctions (ex: Kill Skeleton quest)
16. Ship Weapons - Allows access to ship combat related locations (ex: Ghost Ship voyage)
17. Fishing Rod - Allows location rewards for fishing
18. Shovel - Allows location rewards for digging related locations
19. Pirate Legend - Once achieved, you win

## What is the goal of this game when randomized?

The goal is to defeat The Ghost of Graymarrow at the Fort of the Damned.
However you cannot simply sail to his island, you must first:
* Aquire Emissary Seals by completing a single voyage for specific trading companies
* Aquire the Voyages of Destiny so that you can initiate the Fort of the Damned

The amount of seals required is configurable (0-5). You will learn of which trading company Seals you need upon visiting the Fort of the Damned.


## Which of my items can be in another player's world?

Your world will always contain all 5 faction Seals. Your world will always award you with Pirate Legend upon defeating the Fort of the Damned.

All other items are shuffled.

## How does the game know I complete a check?
The SOT client periodically scans the stats of a ship from Microsoft's website. This is how the data is collected.
When a value for a stat is incremented the client will reward you with the location check and inform the multiworld, this will then allow client sessions to get items at the location.


In order to prevent players from playing out of logic, the client will only allow rewards for locations that are reachable in logic with the current items given to the player. For example, if you need the "Sail" item to get checks off the main island, the client will not allow you to finish checks of the main island. 


This may cause frustration as Microsoft's stat server lags by roughly 5 minutes. So if you just did a check, it may take 5 minutes to recieve the item for the check.
- BE VERY CAREFUL, currently implemented, if you know an item is on a check through a hint, do the check, then go to another location that allows use of that item, the client will assume its not collectable till the multwiorld sends you the item. So do not complete your stuff if the item is not sent to your client

## Unique Local Commands

The following commands are only available when using the Sea of Thieves Client to play with Archipelago. You can list them any time in the client with `/help`.

* `/shop` WIP, opens a shop for players to buy hints
* `/buy #`, WIP, buys an item from the shop
* `/linkShip --name <ship_name> --mscookie <#>`, WIP, Adds tracking of another ship to your multiworld as your player (If you want two players to be able to perform checks on different ships with a shared item/location pool)
* `/linkPirate --name <pirate_name> --mscookie <#>`, WIP, Adds tracking of another pirate to your multiworld as your player (If you want two players to be able to perform checks on different ships with a shared item/location pool)
* `/delinkAll`, WIP, Delinks all tracked accounts from the client
