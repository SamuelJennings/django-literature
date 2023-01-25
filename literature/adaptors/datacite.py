from .base import RemoteAdaptor, DataDict
from ..conf import settings
from datetime import date


class Datacite(RemoteAdaptor):
    BASE_URL = "https://api.datacite.org/dois/{doi}"
    extract_key = "data.attributes"
    author_map = {
        # "orcid": "ORCID",
        # "suffix": "suffix",
        # "prefix": "prefix",
    }
    map = {
        "container_title": "container",
        "date_published": "published",
        "authors": "creators",
        "type": "types.resourceType",
    }

    def modify_authors(self):
        """Need to turn self.data['authors'] into a list of
        author dictionaries
        """
        authors = [
            DataDict(a, keymap=self.author_map) for a in super().modify_authors()
        ]

        x = 8
        return authors

    def author_to_instance(self, author):
        return

    def clean_date_published(self):
        value = self.cleaned_data.get("date_published")
        if not value:
            return None

        # if no month or day data is present, fill with 1s
        date_parts = list(value)
        while len(date_parts) < 3:
            date_parts.append(1)
        return date(*date_parts)


doi = "10.1594/pangaea.807217"
adaptor = Datacite(doi=doi)
x = 8
# pprint.pprint(adaptor.get_defaults())
