import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle
class CannonSanity(Choice):
    """Adds 'On Ship cannon fired' location
    On: Adds a single check for firing the ship cannon
    Basic: Replaces the single check with a check for firing Ball, Blunderbomb, Firebomb, Chain-shot, and player
    Advanced: Basic + any cursed ball + any phantom ball
    No Life: Advanced but the cursed ball and phantom ball checks are replaced with a check on each unique ball (Enable at own risk)"""
    display_name = "Shuffle Cannon Checks"
    option_Off = 0
    option_On_NOT_IMPLEMENTED = 1
    option_Basic = 2
    option_Advanced = 3
    option_No_Life = 4
