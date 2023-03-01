from datetime import date
from pprint import pprint

from django import forms
from django.forms.fields import JSONField

from literature.conf import settings

from .base import BaseAdaptor


class ListConcatField(forms.CharField):
    """Accepts a json array input containing only strings and joins the
    items together using the specified `join_with` parameters.
    """

    def to_python(self, value):
        return super().to_python("".join(value))


class Crossref(BaseAdaptor):
    MAILTO = getattr(settings, "DEFAULT_FROM_EMAIL")
    BASE_URL = "https://api.crossref.org/works/{doi}"
    EXTRACT_KEY = "message"

    MAP = {
        "container_title": "container-title",
        "doi": "DOI",
        "url": "URL",
        "month": "published.date-parts",
        "year": "published.date-parts",
        "published": "published.date-parts",
        "authors": "author",
    }

    # for whatever reason, overriding the year form field in Meta.field_classes won't work
    year = forms.JSONField()
    month = forms.JSONField()

    class Meta(BaseAdaptor.Meta):
        field_classes = {
            "title": ListConcatField,
            "subtitle": ListConcatField,
            "container_title": ListConcatField,
            "published": JSONField,
        }

    def clean_year(self):
        value = self.cleaned_data.get("year")
        if value:
            return value[0][0]

    def clean_month(self):
        value = self.cleaned_data.get("month")
        if value:
            return value[0][1]

    def clean_published(self):
        value = self.cleaned_data.get("published")
        if not value:
            return None

        # if no month or day data is present, fill with 1s
        date_parts = value[0]
        while len(date_parts) < 3:
            date_parts.append(1)
        return date(*date_parts)
