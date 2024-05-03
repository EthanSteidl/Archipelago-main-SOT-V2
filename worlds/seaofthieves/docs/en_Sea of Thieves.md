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

Your items

## Unique Local Commands

The following commands are only available when using the Starcraft 2 Client to play with Archipelago. You can list them any time in the client with `/help`.

* `/download_data` Download the most recent release of the necessary files for playing SC2 with Archipelago. Will overwrite existing files
* `/difficulty [difficulty]` Overrides the difficulty set for the world.
    * Options: casual, normal, hard, brutal
* `/game_speed [game_speed]` Overrides the game speed for the world
    * Options: default, slower, slow, normal, fast, faster
* `/color [faction] [color]` Changes your color for one of your playable factions.
    * Faction options: raynor, kerrigan, primal, protoss, nova
    * Color options: white, red, blue, teal, purple, yellow, orange, green, lightpink, violet, lightgrey, darkgreen, brown, lightgreen, darkgrey, pink, rainbow, random, default
* `/option [option_name] [option_value]` Sets an option normally controlled by your yaml after generation.
    * Run without arguments to list all options.
    * Options pertain to automatic cutscene skipping, Kerrigan presence, Spear of Adun presence, starting resource amounts, controlling AI allies, etc.
* `/disable_mission_check` Disables the check to see if a mission is available to play. Meant for co-op runs where one player can play the next mission in a chain the other player is doing.
* `/play [mission_id]` Starts a Starcraft 2 mission based off of the mission_id provided
* `/available` Get what missions are currently available to play
* `/unfinished` Get what missions are currently available to play and have not had all locations checked
* `/set_path [path]` Manually set the SC2 install directory (if the automatic detection fails)
