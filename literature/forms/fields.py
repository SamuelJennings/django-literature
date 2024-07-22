import ast
import json

from citeproc.source.json import CiteProcJSON
from django import forms
from django.core.exceptions import ValidationError
from django_select2.forms import Select2TagWidget

from ..utils import parse_author
from ..utils.date import iso_to_date_parts
from .widgets import DateVariableWidget, PartialDateWidget


class PartialDateFormField(forms.CharField):
    """A form field that provides separate fields for day, month, and year. Values from the separate fields are combined into a value suitable for a partial_date.PartialDateField."""

    widget = PartialDateWidget

    def to_python(self, value):
        # return "-".join(value) if value else None
        return super().to_python(value)


class CSLDateField(forms.Field):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        self.fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        self.widget = forms.Textarea()

    def to_python(self, value):
        if not value:
            return None
        try:
            data = json.loads(value)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON data")

        return CiteProcJSON.parse_date(self, data)

    def validate(self, value):
        super().validate(value)
        if self.model and self.fields:
            for item in value:
                for field in self.fields:
                    if field not in item:
                        raise ValidationError(f"Missing field {field} in item {item}")


class NameWidget(Select2TagWidget):
    def optgroups(self, name, values, attrs=None):
        selected = set(values)
        subgroup = [self.create_option(name, v, v, selected, i) for i, v in enumerate(values)]
        return [(None, subgroup, 0)]

    def create_option(self, name, value, label, selected, index):
        author = ast.literal_eval(value)
        value = "{given} {particle} {family} {suffix}".format(
            given=author.get("given", ""),
            particle=author.get("non-dropping-particle", ""),
            family=author.get("family", ""),
            suffix=author.get("suffix", ""),
        ).strip()
        option = super().create_option(name, value, value, selected, index)
        return option


class NameField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = NameWidget(attrs={"data-token-separators": ","})

    def to_python(self, value):
        if value is None:
            return None
        processed = []
        for val in value:
            if isinstance(val, dict):
                processed.append(val)
            else:
                val = str(val).strip()
                processed.append({k: v for k, v in parse_author(val).items() if v})
        return processed

    def prepare_value(self, value):
        return value


class DateVariableField(forms.MultiValueField):
    widget = DateVariableWidget

    def __init__(self, *args, **kwargs):
        fields = (
            PartialDateFormField(label="begin", required=False),
            PartialDateFormField(label="end", required=False),
            forms.CharField(label="season", required=False),
            forms.CharField(label="literal", required=False),
            forms.BooleanField(label="circa", initial=False, required=False),
        )
        return super().__init__(fields=fields, *args, **kwargs)

    def compress(self, data_list):
        # takes a list of values from the fields above and returns a single value
        # that will be saved to the form/model field
        begin, end, season, raw, circa = data_list

        csl = {}

        date_parts = []
        if begin:
            date_parts.append(iso_to_date_parts(begin))
        if end:
            date_parts.append(iso_to_date_parts(end))

        if date_parts:
            csl["date-parts"] = date_parts
        if season:
            csl["season"] = season
        if raw:
            csl["raw"] = raw
        if circa:
            csl["circa"] = circa

        return csl
