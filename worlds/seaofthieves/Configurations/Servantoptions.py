
import Options
from .OptionsBase import ChoiceForEach

DefaultOffToggle = Options.Toggle


class ServantSanity(ChoiceForEach):
    """Adds 'On Hourglass Guardian of Fortune Sunk' location
    On For Each: replaces the On Hourglass Guardian of Fortune Sunk check with a check on Guardian of Fortune sloop, brig, and galleon check
    """
    display_name = "(PVP) Servant"
    default = 1
