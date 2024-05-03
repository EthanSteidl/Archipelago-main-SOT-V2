class SotLoginCredentials:

    def __init__(self, msCookie: str):
        self.msCookie = msCookie

class SotAnalyzerDetails:

    def __init__(self, shipName: str | None, pirateName: str | None):
        self.shipName: str | None = shipName
        self.pirateName: str | None = pirateName

    def set_pirate(self, name: str) -> None:
        self.pirateName = name
        self.shipName = None

    def set_ship(self, name: str) -> None:
        self.shipName = name
        self.pirateName = None

    def get_ship(self) -> str | None:
        return self.shipName

    def get_pirate(self) -> str | None:
        return self.pirateName

class UserInformation:

    def __init__(self, sotLoginCreds: SotLoginCredentials, sotAnalyzerDetails: SotAnalyzerDetails, address: str):
        self.loginCreds = sotLoginCreds
        self.analyzerDetails = sotAnalyzerDetails
        self.address = address