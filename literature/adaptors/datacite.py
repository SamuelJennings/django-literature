from datetime import date

from ..conf import settings
from .base import BaseAdaptor, DataDict


class Datacite(BaseAdaptor):
    BASE_URL = "https://api.datacite.org/dois/{doi}"
    EXTRACT_KEY = "data.attributes"
    AUTHOR_MAP = {
        "given": "givenName",
        "family": "familyName",
    }
    MAP = {
        "container_title": "container",
        "year": "published",
        "authors": "creators",
        "type": "types.resourceType",
    }

    def premodify_data(self, data):
        data = super().premodify_data(data)
        data["authors"] = [DataDict(a, self.AUTHOR_MAP) for a in data["authors"]]
        return data

    def clean_published(self):
        value = self.cleaned_data.get("published")
        if not value:
            return None

        # if no month or day data is present, fill with 1s
        date_parts = list(value)
        while len(date_parts) < 3:
            date_parts.append(1)
        return date(*date_parts)
