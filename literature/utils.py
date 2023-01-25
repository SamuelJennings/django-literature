from collections import UserDict
from urllib.parse import urlparse

from django.utils.module_loading import import_string

from literature.conf import settings


class DataDict(UserDict):
    """A custom python dict that takes a keymap

    Args:
        UserDict (_type_): _description_
    """

    def __init__(self, dict=None, /, **kwargs):
        self.keymap = kwargs.pop("keymap")
        return super().__init__(dict, **kwargs)

    def __getitem__(self, key):
        if key in self.keymap.keys():
            data = self.data
            for k in self.keymap[key].split("."):
                data = data[k]
        else:
            data = self.data[key]
        return data


def clean_doi(doi):
    """Uses `urllib.parse.urlparse` to extract a DOI from a string. Trailing slashes
    are removed using the string.strip() method and the output is converted to
    lowercase.

    Args:
        doi (string): An unformated string containing a DOI.

    Returns:
        doi: A cleaned DOI string
    """
    return urlparse(doi).path.strip("/").lower()


def autolabel_strategy(obj):
    """The strategy used to create unique labels for literature items in the
    database.

    TODO: This has not been implemented yet

    Args:
        obj (literature.models.Literature): A Literature instance.
    """
    label = obj.label

    # We don't want label clashes so find how many labels already
    # in the database start with our new label then append the
    # appropriate letter.
    letters = "abcdefghijklmopqrstuvwzy"
    count = obj._meta.model.objects.filter(label__startswith=label).count()
    if count:
        label += letters[count + 1]

    return


def simple_title_renamer(instance, fname):
    return f"literature/{instance.title[:50]}.pdf"


def pdf_file_renamer(instance, fname):
    func = import_string(settings.LITERATURE_PDF_RENAMER)
    return func(instance, fname)
