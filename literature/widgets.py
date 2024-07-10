from citeproc.source.json import CiteProcJSON
from django import forms
from partial_date import PartialDate

from .models import Date
from .utils import django_lit_to_csl


def get_partial_iso_date(date_dict):
    date = str(date_dict["year"])
    if "month" in date_dict:
        date += "-{:02}".format(date_dict["month"])
        if "day" in date_dict:
            date += "-{:02}".format(date_dict["day"])

    return date


DATE_FIELDS = ["type", "begin", "end", "literal", "season", "circa", "raw"]


class CSLDateWidget(forms.TextInput):
    def __init__(self, **kwargs):
        return super().__init__(attrs={"type": "date"}, **kwargs)

    def format_value(self, value):
        if value:
            return value.strftime("%Y-%m-%d")
        return None

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if not value:
            return None

        value = django_lit_to_csl(value)
        value = CiteProcJSON.parse_date(None, value)
        if "year" in value:
            value["begin"] = PartialDate(get_partial_iso_date(value))
        elif "begin" in value:
            value["begin"] = PartialDate(get_partial_iso_date(value["begin"]))

        if "end" in value:
            value["end"] = PartialDate(get_partial_iso_date(value["end"]))
        value["type"] = name
        return {k: v for k, v in value.items() if k in DATE_FIELDS}


class CSLDateField(forms.ModelChoiceField):
    widget = CSLDateWidget

    def __init__(self, *args, **kwargs):
        kwargs["queryset"] = Date.objects.all()
        return super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or "pk"
            if isinstance(value, self.queryset.model):
                value = getattr(value, key)
            # value = self.queryset.get_or_create(**{key: value}, )
            value = self.queryset.model(**value)
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            pass
            # raise ValidationError(
            #     self.error_messages["invalid_choice"],
            #     code="invalid_choice",
            #     params={"value": value},
            # )
        return value
