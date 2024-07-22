from django import forms
from django.forms import Widget
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from partial_date import PartialDate

from literature.utils.date import date_parts_to_iso, parse_date


class PartialDateWidget(forms.SelectDateWidget):
    def __init__(self, **kwargs):
        empty_labels = [_("Year"), _("Month"), _("Day")]
        return super().__init__(empty_label=empty_labels, **kwargs)

    def get_context(self, name, value, attrs):
        # reorder the subwidgets to year, month, day
        context = super().get_context(name, value, attrs)
        m, d, y = context["widget"]["subwidgets"]
        context["widget"]["subwidgets"] = [y, m, d]
        return context

    def format_value(self, value):
        # convert PartialDate to dict for SelectDateWidget
        if isinstance(value, PartialDate):
            return {
                "year": value.date.year,
                "month": value.date.month if value.precision >= PartialDate.MONTH else None,
                "day": value.date.day if value.precision == PartialDate.DAY else None,
            }
        elif isinstance(value, dict):
            return value
        return {"year": None, "month": None, "day": None}


class DateArrayWidget(PartialDateWidget):
    def value_from_datadict(self, data, files, name):
        return super().value_from_datadict(data, files, name).split("-")


class FlatJSONWidget(Widget):
    """
    A widget that displays key/value pairs from JSON as a list of text input
    box pairs and back again.
    """

    template_name = "literature/widgets/attributes.html"
    row_template = "literature/widgets/{style}_attributes_row.html"
    style = "bootstrap5"

    @property
    def media(self):
        js = ["literature/js/key-value-widget.js"]
        return forms.Media(js=js)

    # Heavily modified from a code snippet by Huy Nguyen:
    # https://www.huyng.com/posts/django-custom-form-widget-for-dictionary-and-tuple-key-value-pairs
    def __init__(self, *args, **kwargs):
        """
        Supports additional kwargs: `key_attr`, `val_attr`, `sorted`.
        """
        self.key_attrs = kwargs.pop("key_attrs", {})
        self.val_attrs = kwargs.pop("val_attrs", {})
        self.sorted = sorted if kwargs.pop("sorted", True) else lambda x: x
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        if not value:
            value = "{}"

        if attrs is None:
            attrs = {}

        context = super().get_context(name, value, attrs)

        context["content"] = ""

        # value = ast.literal_eval(value)
        if value and isinstance(value, dict) and len(value) > 0:
            for key in self.sorted(value):
                context["content"] += render_to_string(
                    self.row_template.format(style=self.style),
                    context={
                        "key": escape(key),
                        "value": escape(value[key]),
                        "field_name": name,
                        "key_attrs": flatatt(self.key_attrs),
                        "val_attrs": flatatt(self.val_attrs),
                    },
                )
        context["content"] = mark_safe(context["content"])
        return context

    def value_from_datadict(self, data, files, name):
        """
        Returns the dict-representation of the key-value pairs
        sent in the POST parameters

        :param data: (dict) request.POST or request.GET parameters.
        :param files: (list) request.FILES
        :param name: (str) the name of the field associated with this widget.
        """
        key_field = f"attributes_key[{name}]"
        val_field = f"attributes_value[{name}]"
        if key_field in data and val_field in data:
            keys = data.getlist(key_field)
            values = data.getlist(val_field)
            return dict([item for item in zip(keys, values) if item[0] != ""])
        return {}

    def value_omitted_from_data(self, data, files, name):
        return False


class DateVariableWidget(forms.MultiWidget):
    template_name = "literature/widgets/csl_date.html"

    def __init__(self, attrs=None):
        widgets = {
            "begin": PartialDateWidget,
            "end": PartialDateWidget,
            "season": forms.TextInput,
            "literal": forms.TextInput,
            "circa": forms.CheckboxInput,
        }
        super().__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        result = []

        if name in data:
            parsed = parse_date(data[name])

            # handle the case when the date value is supplied as a CSL date variable
            return [
                date_parts_to_iso(parsed.get("begin")),
                date_parts_to_iso(parsed.get("end")),
                parsed.get("literal"),
                parsed.get("season"),
                parsed.get("circa", False),
            ]
        else:
            # treat it like a typical django-literature form
            for widget_name, widget in zip(self.widgets_names, self.widgets):
                value = widget.value_from_datadict(data, files, name + widget_name)
                result.append(value)
            return result

    def decompress(self, value):
        if not value:
            return [None] * len(self.widgets)

        parsed = parse_date(value)
        return [
            parsed.get("begin"),
            parsed.get("end"),
            parsed.get("literal"),
            parsed.get("season"),
            parsed.get("circa", False),
        ]
