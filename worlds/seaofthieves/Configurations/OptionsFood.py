import typing
from dataclasses import dataclass

import Options
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle, TextChoice

DefaultOffToggle = Options.Toggle
class MunchSanity(DefaultOffToggle):
    """Adds the 'On Eat' location for categories of Fruit, Fish, Seamonster, Land Animal, Bugs"""
    display_name = "Shuffle (EAT) Checks"
class MunchSanityFruit(DefaultOffToggle):
    """If shuffle EAT, removes on eat fruit check, adds a check on each fruit"""
    display_name = "(EAT) Fruit"
class MunchSanityFish(DefaultOffToggle):
    """If shuffle EAT, removes on eat fish check, adds a check on each type of fish"""
    display_name = "(EAT) Fish"
class MunchSanitySeamonster(DefaultOffToggle):
    """If shuffle EAT, removes on eat seamonster check, adds a check on each seamonster"""
    display_name = "(EAT) Seamonster"
class MunchSanityLandAnimal(DefaultOffToggle):
    """If shuffle EAT, removes on eat land animal check, adds a check on each land animal"""
    display_name = "(EAT) Animal"
class MunchSanityBug(DefaultOffToggle):
    """If shuffle EAT, removes on eat Bug check, adds a check on each Bug"""
    display_name = "(EAT) Bug"



class CookSanity(DefaultOffToggle):
    """Adds the 'On Cook' location for categories of Fish, Seamonster, Land Animal"""
    display_name = "Shuffle (COOK) Checks"
class CookSanityFish(DefaultOffToggle):
    """If shuffle COOK, removes on cook fish check, adds a check on each fish"""
    display_name = "(COOK) Fish"
class CookSanitySeamonster(DefaultOffToggle):
    """If shuffle COOK, removes on cook fish check, adds a check on each type of fish"""
    display_name = "(COOK) Seamonster"
class CookSanityLandAnimal(DefaultOffToggle):
    """If shuffle COOK, removes on cook land animal check, adds a check on each land animal"""
    display_name = "(COOK) Animal"



class BurnSanity(DefaultOffToggle):
    """Adds the 'On Burn' location for categories of Fish, Seamonster, Land Animal"""
    display_name = "Shuffle (BURN) Checks"
class BurnSanityFish(DefaultOffToggle):
    """If shuffle Burn, removes on Burn fish check, adds a check on each fish"""
    display_name = "(BURN) Fish"
class BurnSanitySeamonster(DefaultOffToggle):
    """If shuffle Burn, removes on Burn fish check, adds a check on each type of fish"""
    display_name = "(BURN) Seamonster"
class BurnSanityLandAnimal(DefaultOffToggle):
    """If shuffle Burn, removes on Burn land animal check, adds a check on each land animal"""
    display_name = "(BURN) land animal"

