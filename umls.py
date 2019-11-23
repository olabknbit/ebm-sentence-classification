BASE_UMLS_URL = 'https://uts-ws.nlm.nih.gov'


class UMLS:
    def __init__(self):
        self.auth_client, self.tgt = self.authenticate_umls()

    def authenticate_umls(self):
        # TODO sort imports out
        from authentication import Authentication
        import creds
        auth = Authentication(apikey=creds.apikey)
        tgt = auth.gettgt()
        return auth, tgt

    def get_response(self, endpoint, args=''):
        import requests
        import json

        query = {'ticket': self.auth_client.getst(self.tgt)}
        r = requests.get(BASE_UMLS_URL + endpoint + args, params=query)

        r.encoding = 'utf-8'

        items = json.loads(r.text)
        return items["result"]

    def retrieve_cuis(self, text='fracture of carpal bone'):
        endpoint = '/rest/search/current?string=' + text
        result = self.get_response(endpoint, args='&returnIdType=code')

        results = result["results"]
        cuis = [result["ui"] for result in results]
        cuis = list(filter(lambda x: x != 'NONE', cuis))
        return cuis


if __name__ == '__main__':
    c = UMLS()
    search_phrase = 'fracture of carpal bone'
    response = c.get_response(endpoint='/rest/search/current?string=' + search_phrase)
    import json
    print(json.dumps(response, indent=2, sort_keys=True))
