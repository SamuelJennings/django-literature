import json
from pprint import pprint
from urllib.parse import urlparse

f = 'litman/tests/data/crossref.json'

with open(f, 'r') as f:
    cr = json.load(f)['message']



class DictMap(object):

    map = {
        'container_title': 'container-title',
        'doi': 'DOI',
        'published': 'published.date-parts',
        }

    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):

        data = self.data
        for subkey in self.map[key].split('.'):
            data = data[subkey]

        if hasattr(self, f"clean_{key}"):
            return getattr(self, f"clean_{key}")(data)

        return data

    def clean_doi(self, val):
        return urlparse(val).path.strip("/").lower()

    def clean_container_title(self, val):
        return "".join(val)


adapter = DictMap(cr)

# for i in DictMap.map.keys():
    # print(adapter[i])

pprint(adapter.__dict__)