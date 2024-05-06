import typing
from dataclasses import dataclass

import Options
from Options import Choice
from .OptionsBase import ChoiceForEach
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle

class CannonSanityBalls(ChoiceForEach):
    """Adds a check on firing a Ball, Blunderbomb, or Firebomb. If For Each, adds a check instead on firing each type."""
    display_name = "(CAN) Balls"

class CannonSanityCursed(ChoiceForEach):
    """Adds a check on firing a Cursed Ball. If For Each, adds a check instead on firing each type."""
    display_name = "(CAN) Cursed"

class CannonSanityPhantom(ChoiceForEach):
    """Adds a check on firing a Phantom Ball. If For Each, adds a check instead on firing each type."""
    display_name = "(CAN) Phantom"