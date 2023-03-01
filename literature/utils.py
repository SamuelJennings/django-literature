import copy
from collections import UserDict
from datetime import datetime

from django.utils.module_loading import import_string

from literature.conf import settings


class DataDict(UserDict):
    """A custom python dict that takes a keymap

    Args:
        UserDict (_type_): _description_
    """

    def __init__(self, dict=None, keymap={}):
        self.keymap = keymap
        return super().__init__(dict)

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
    # NOTE: This only works for strings starting with http://. This will not
    # correctly for strings like doi.org/... or www.doi,org/...
    # swith to tldextract??

    return doi.split("doi.org/")[-1].strip("/").lower()
    # return urlparse(doi).path.strip("/").lower()


def simple_autolabeler(obj):
    """The strategy used to create unique labels for literature items in the
    database.

    TODO: This has not been implemented yet

    Args:
        obj (literature.models.Literature): A Literature instance.
    """
    label = f"{obj.authors.first().family}{obj.year}"
    # We don't want label clashes so find how many labels already
    # in the database start with our new label then append the
    # appropriate letter.
    letters = "abcdefghijklmopqrstuvwzy"
    count = obj._meta.model.objects.filter(label__startswith=label).count()

    if count:
        label += letters[count]

    return label


def simple_file_renamer(instance, fname):
    return f"literature/{instance.title[:50].strip()}.pdf"


def pdf_file_renamer(instance, fname=None):
    func = import_string(settings.LITERATURE_PDF_RENAMER)
    return func(instance, fname)


def get_current_year():
    return datetime.now().year
