import typing
from dataclasses import dataclass

import Options
from .OptionsBase import ChoiceForEach

DefaultOffToggle = Options.Toggle


class FishSanity(ChoiceForEach):
    """Adds 'On Fish Caught' location
    On For Each: replaces the on caught check with on caught for each fish
    No Life: replaces the on caught check with on caught for each descriptor+fish (Will add hours to your run)"""
    display_name = "Shuffle Catch Fish Checks"
    default = 1
    option_No_Life = 3
