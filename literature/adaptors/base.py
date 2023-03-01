import requests
from django.apps import apps
from django.forms import ModelForm, ModelMultipleChoiceField
from django.utils.translation import gettext as _

from ..exceptions import AdaptorError, RemoteAdaptorError
from ..models import Author
from ..utils import DataDict, clean_doi


class AuthorField(ModelMultipleChoiceField):
    def prepare_value(self, value):
        """Convert a list of author dicts to model instances.

        Args:
            value (list): A list of dicts containing form data

        Raises:
            ValidationError: If the form fails to validate

        Returns:
            list: A list of ids of the saved entries
        """
        if not value:
            return

        model = self.queryset.model
        fields = [
            "given",
            "family",
            "ORCID",
        ]
        obj_ids = []
        for obj in value:
            data = {f: obj[f] for f in fields if obj.get(f)}

            instance, _ = model.objects.update_or_create(
                given=data.pop("given"),
                family=data.pop("family"),
                defaults=data,
            )
            obj_ids.append(instance.id)
        return obj_ids


class BaseAdaptor(ModelForm):
    BASE_URL = None
    EXTRACT_KEY = ""
    SOURCE = ""
    MAP = {}
    AUTHOR_MAP = {}

    authors = AuthorField(queryset=Author.objects.all())

    class Meta:
        model = apps.get_model("literature.Literature")
        # fields = "__all__"
        exclude = ["label"]

    def __init__(self, data=None, *args, **kwargs):
        if kwargs.get("doi"):
            data = self.resolve_doi(kwargs.pop("doi"))
        data = self.premodify_data(data)
        super().__init__(data, *args, **kwargs)

    @property
    def is_remote(self):
        return self.BASE_URL is not None

    def premodify_data(self, data):
        return DataDict(data, keymap=self.MAP)

    def full_clean(self):
        self.data["authors"] = self.modify_authors()
        return super().full_clean()

    def modify_authors(self):
        authors = self.data["authors"]
        return authors

    def clean_doi(self):
        doi = self.cleaned_data["doi"]
        return clean_doi(doi)

    def get_data(self):
        self.is_valid()
        return self.cleaned_data, self.errors

    def resolve_doi(self, doi):
        """Resolve a doi at the specified BASE_URL

        Args:
            doi (string): a Digital Object Identifier (DOI) for an online resource

        Returns:
            response (object): a `requests` response object
        """
        if not self.is_remote:
            raise AdaptorError(_(f"{self} cannot resolve remote sources."))
        response = requests.get(self.BASE_URL.format(doi=doi))
        if not response.status_code == 200:
            raise RemoteAdaptorError(response.text)
        data = response.json()
        if self.EXTRACT_KEY:
            for attr in self.EXTRACT_KEY.split("."):
                data = data[attr]
        return data


# class FileAdaptor(RemoteAdaptor):
