class SotLoginCredentials:

    def __init__(self, msCookie: str):
        self.msCookie = msCookie

class SotAnalyzerDetails:

    def __init__(self, shipName: str):
        self.shipName = shipName

class UserInformation:

    def __init__(self, sotLoginCreds: SotLoginCredentials, sotAnalyzerDetails: SotAnalyzerDetails, address: str):
        self.loginCreds = sotLoginCreds
        self.analyzerDetails = sotAnalyzerDetails
        self.address = address