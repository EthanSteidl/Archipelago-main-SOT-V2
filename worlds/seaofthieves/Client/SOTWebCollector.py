


import requests
import time
import random
import json
import UserInformation


class SOTWebCollector:
    AUTH = r'www.seaofthieves.com'
    METH = r'GET'
    PATH = r'/api/profilev2/captaincy'
    SCHEME = r'https'
    ACCEPT = r'*/*'
    ACCEPT_ENCODING = r'gzip, deflate, br, zstd'
    ACCEPT_LANGUAGE = r'en-US,en;q=0.9'
    IF_NONE_MATCH = r'W/"48e7b-Aia4dpCjBkRq7clT7iALW7VKlcg"'
    REFERER = r'https://www.seaofthieves.com/profile/captaincy'
    SEE_CH_UA = r'"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"'
    SEE_CH_UA_mobile = r'?0'
    SEE_CH_UA_PLATFORM = r'"Windows"'
    SEC_FETCH_DEST = r'empty'
    SEC_FETCH_MODE = r'cors'
    SEC_FETCH_SITE = r'same-origin'
    USER_AGENT = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

    def __init__(self, loginCreds: UserInformation.SotLoginCredentials):
        self.loginCreds = loginCreds
        self.lastQueryTimeSeconds = -10000
        self.json = {}

    def getHeaders(self):
        headers = {
            "authority": self.AUTH,
            "method": self.METH,
            "path": self.PATH,
            "scheme": self.SCHEME,
            "Accept": self.ACCEPT,
            "Accept-Encoding": self.ACCEPT_ENCODING,
            "Accept-Language": self.ACCEPT_LANGUAGE,
            "Cookie": self.loginCreds.msCookie,
            "If-None-Match": self.IF_NONE_MATCH,
            "Referer": self.REFERER,
            "Sec-Ch-Ua": self.SEE_CH_UA,
            "Sec-Ch-Ua-Mobile": self.SEE_CH_UA_mobile,
            "Sec-Ch-Ua-Platform": self.SEE_CH_UA_PLATFORM,
            "Sec-Fetch-Dest": self.SEC_FETCH_DEST,
            "Sec-Fetch-Mode": self.SEC_FETCH_MODE,
            "Sec-Fetch-Site": self.SEC_FETCH_SITE,
            "User-Agent": self.USER_AGENT,

            "Cache-Control": "max-age=0"

        }
        return headers


    def getJson(self):
        if(self.json is None or self.lastQueryTimeSeconds+5 < time.time() ):
            try:
                resp = requests.get('https://www.seaofthieves.com/api/profilev2/captaincy', headers=self.getHeaders())
                text = resp.text
                self.json = json.loads(text)
                #with open('sottempdata.json', 'w') as f:
                #    self.json.dump(self.json, f)
            except:
                print("The query to the web server failed, resolution steps: (1) enter the correct cookie (2) open the Captaincy page on www.seaofthieves.com")

            self.lastQueryTimeSeconds = time.time()
        return self.json