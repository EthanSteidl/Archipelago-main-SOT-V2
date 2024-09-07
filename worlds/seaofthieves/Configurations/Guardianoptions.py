import typing
from dataclasses import dataclass

import Options
from Options import Choice
from .OptionsBase import ChoiceForEach
DefaultOffToggle = Options.Toggle


class GuardianSanity(ChoiceForEach):
    """Adds 'On Hourglass Servant of Flame Sunk' location
    On For Each: replaces the On Hourglass Servant of Flame Sunk check with a check on Guardian of Fortune sloop, brig, and galleon check
    """
    display_name = "(PVP) Guardian"
    default = 1
