from .base import RemoteAdaptor, DataDict
from litman.conf import settings
from datetime import date
from django import forms
from django.forms.fields import JSONField


class ListConcatField(forms.CharField):
    """Accepts a json array input containing only strings and joins the
    items together using the specified `join_with` parameters.
    """
    # default_validators = [validate_json, PythonTypeValidator(list)]

    def to_python(self, value):
        return super().to_python(''.join(value))


class Crossref(RemoteAdaptor):
    MAILTO = getattr(settings, 'DEFAULT_FROM_EMAIL')
    BASE_URL = "https://api.crossref.org/works/{doi}"
    extract_key = 'message'
    author_map = {
        "orcid": "ORCID",
        "suffix": "suffix",
        "givenName": "given",
        "familyName": "family",
        "name": "name",
        "prefix": "prefix",
    }
    map = {
        'container_title': 'container-title',
        'doi': 'DOI',
        'url': 'URL',
        'date_published': 'published.date-parts',
        'authors': 'author',
    }

    class Meta(RemoteAdaptor.Meta):
        field_classes = {
            'title': ListConcatField,
            'subtitle': ListConcatField,
            'container_title': ListConcatField,
            'date_published': JSONField,
        }

    def modify_authors(self):
        """Need to turn self.data['authors'] into a list of
        author dictionaries
        """
        authors = [DataDict(a, keymap=self.author_map)
                   for a in super().modify_authors()]

        x = 8
        return authors

    def author_to_instance(self, author):
        return

    def clean_date_published(self):
        value = self.cleaned_data.get('date_published')
        if not value:
            return None

        # if no month or day data is present, fill with 1s
        date_parts = value[0]
        while len(date_parts) < 3:
            date_parts.append(1)
        return date(*date_parts)

    def clean_authors(self):
        author_list = self.data.get('author')
        return


doi = "https://doi.org/10.1093/gji/ggz376"
adaptor = Crossref(doi=doi)

adaptor.is_valid()

# pprint.pprint(adaptor.cleaned_data)
# pprint.pprint(adaptor.get_defaults())
