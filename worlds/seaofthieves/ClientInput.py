

from .Configurations import SotOptionsDerived
import typing
import pickle
from .Regions.ConnectionDetails import ConnectionDetails
class ClientInput:

    def __init__(self):
        self.sotOptionsDerived = None
        self.regionRules = None

    def to_file(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
    def from_fire(self, filename: str):
        with open(filename, 'rb') as f:
            clientInput = pickle.load(f)
        self.sotOptionsDerived = clientInput.sotOptionsDerived
        self.regionRules = clientInput.regionRules
