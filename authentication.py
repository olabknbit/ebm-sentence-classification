#!/usr/bin/python
# See https://documentation.uts.nlm.nih.gov/rest/authentication.html for full explanation

import requests
from lxml.html import fromstring

uri = "https://utslogin.nlm.nih.gov"
auth_endpoint = "/cas/v1/api-key"


class Authentication:
    def __init__(self, apikey):
        self.apikey = apikey
        self.service = "http://umlsks.nlm.nih.gov"

    def gettgt(self):
        params = {'apikey': self.apikey}
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        r = requests.post(uri + auth_endpoint, data=params, headers=h)
        response = fromstring(r.text)
        tgt = response.xpath('//form/@action')[0]
        return tgt

    def getst(self, tgt):
        params = {'service': self.service}
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        r = requests.post(tgt, data=params, headers=h)
        st = r.text
        return st
