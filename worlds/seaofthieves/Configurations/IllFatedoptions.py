import typing
from dataclasses import dataclass

import Options

DefaultOffToggle = Options.Toggle


class IllFated(DefaultOffToggle):
    """Adds locations related to your ship sinking
    """
    display_name = "Shuffle Ill-Fated Checks"
