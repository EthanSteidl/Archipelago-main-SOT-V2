import typing
from dataclasses import dataclass

import Options
from OptionsBase import ChoiceForEach

DefaultOffToggle = Options.Toggle


class RowboatSanity(ChoiceForEach):
    """Adds 'On Rowboat Dock' location
    On For Each: replaces the On Rowboat Dock check with a check on each unique rowboat (Lantern, Harpoon, Cannon)
    """
    display_name = "Rowboats"
    default = 1
