import json

import requests
from django.apps import apps
from django.forms import ModelForm

from ..utils import DataDict, clean_doi


class AdaptorError(Exception):
    """The requested model field does not exist"""

    pass


class RemoteAdaptorError(Exception):
    """The requested model field does not exist"""

    pass


class BaseAdaptor(ModelForm):
    source = ""
    map = {}

    class Meta:
        model = apps.get_model("literature.Work")
        fields = "__all__"

    def __init__(self, data, *args, **kwargs):
        data = self.get_data(data, **kwargs)
        super().__init__(data, *args, **kwargs)

    def full_clean(self):
        self.data["data"] = json.dumps(self.data, default=dict)

        self.data["authors"] = self.modify_authors()

        return super().full_clean()

    def modify_authors(self):
        authors = self.data["authors"]
        return authors

    def clean_doi(self, val):
        doi = self.cleaned_data["doi"]
        return clean_doi(doi)

    def get_data(self, data):
        return DataDict(data, keymap=self.map)


class RemoteAdaptor(BaseAdaptor):
    BASE_URL = None
    extract_key = ""

    class Meta(BaseAdaptor.Meta):
        pass

    def __init__(self, data=None, doi=None, *args, **kwargs):
        data = self.get_data(data, doi)
        super().__init__(data, *args, **kwargs)

    def get_data(self, data=None, doi=None):
        if doi:
            data = self.resolve(doi)
        return super().get_data(data)

    def extract(self, response):
        """Extract the data object from the reolved DOI response.

        Args:
            response (_type_): _description_

        Returns:
            data: The data object from the resource
        """
        data = response.json()
        if self.extract_key:
            for attr in self.extract_key.split("."):
                data = data[attr]
        return data

    def resolve(self, doi):
        """Resolve a doi at the specified BASE_URL

        Args:
            doi (string): a Digital Object Identifier (DOI) for an online resource

        Returns:
            response (object): a `requests` response object
        """
        response = requests.get(self.BASE_URL.format(doi=doi))
        return self.extract(response)


# class FileAdaptor(RemoteAdaptor):
