

import typing
from dataclasses import dataclass
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

class ShipSanity(DefaultOnToggle):
    """Adds player ship related checks"""
    display_name = "Player Ship Locations"
    default = 1

