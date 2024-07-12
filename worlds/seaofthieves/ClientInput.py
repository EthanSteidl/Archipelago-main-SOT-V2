from .Configurations import SotOptionsDerived
import typing
import pickle
from .Regions.ConnectionDetails import ConnectionDetails
from .MultiworldHints import MultiworldHints

class ClientInput:

    def __init__(self):
        self.sotOptionsDerived = None
        self.regionRules = None
        self.multiworldHints: typing.Optional[MultiworldHints] = None

    def to_file(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def from_fire(self, filename: str):
        with open(filename, 'rb') as f:
            clientInput = pickle.load(f)
        self.sotOptionsDerived = clientInput.sotOptionsDerived
        self.regionRules = clientInput.regionRules
        self.multiworldHints = clientInput.multiworldHints

    def hasEnoughToPlay(self) -> bool:
        return self.sotOptionsDerived is not None and self.regionRules is not None
