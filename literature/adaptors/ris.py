from .base import BaseAdaptor


class RISAdaptor(BaseAdaptor):
    MAP = {
        "container_title": "container-title",
        "doi": "DOI",
        "url": "URL",
        "date_published": "published.date-parts",
        "authors": "author",
    }
