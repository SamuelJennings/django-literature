import json

from citeproc.source.json import CiteProcJSON
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.widgets import Select
from django.utils.translation import gettext_lazy as _
from django_select2.forms import ModelSelect2MultipleWidget
from partial_date import PartialDate

from .models import Name


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
        return {"year": None, "month": None, "day": None}

    def value_from_datadict(self, data, files, name):
        # build a PartialDate from the separate fields

        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if y == m == d == "":
            return None

        # build the date string
        value = y
        if m:
            value += f"-{m}"
        if m and d:
            value += f"-{d}"

        return value


class PartialDateFormField(forms.CharField):
    """A form field that provides separate fields for day, month, and year. Values from the separate fields are combined into a value suitable for a partial_date.PartialDateField."""

    widget = PartialDateWidget


class PageRangeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(attrs={"placeholder": "Start Page"}),
            forms.NumberInput(attrs={"placeholder": "End Page"}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split("-")
        return [None, None]

    def format_output(self, rendered_widgets):
        return f'<div class="page-range">{rendered_widgets[0]} - {rendered_widgets[1]}</div>'


class PageRangeField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = [
            forms.IntegerField(),
            forms.IntegerField(),
        ]
        widget = PageRangeWidget()
        super().__init__(fields=fields, widget=widget, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            page_start, page_end = data_list
            if page_start > page_end:
                raise ValidationError(_("Start page must not be greater than end page"))
            return f"{page_start}-{page_end}"
        return ""

    def clean(self, value):
        cleaned_data = super().clean(value)
        page_start, page_end = cleaned_data
        if page_start > page_end:
            raise ValidationError(_("Start page must not be greater than end page"))
        return f"{page_start}-{page_end}"


class Select2Widget(Select):
    def __init__(self, attrs=None, choices=()):
        default_attrs = {"class": "select2", "style": "width:450px;"}
        if attrs:
            attrs.update(default_attrs)
        else:
            attrs = default_attrs
        super().__init__(attrs, choices)

    class Media:
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css",
                "https://cdn.jsdelivr.net/npm/select2-bootstrap-5-theme@1.3.0/dist/select2-bootstrap-5-theme.min.css",
            )
        }
        js = (
            settings.SELECT2_JS or []
            # "ror/js/select2_init.js",
        )


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


class CSLNameField(forms.Field):
    def to_python(self, value):
        if not value:
            return None
        return CiteProcJSON.parse_names(self, value)


class AuthorWidget(ModelSelect2MultipleWidget):
    # def value_from_datadict(self, data: dict[str, Any], files: Mapping[str, Iterable[Any]], name: str) -> Any:
    #     return super().value_from_datadict(data, files, name)

    pass


class NameField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            queryset=Name.objects.all(),
            required=False,
            **kwargs,
        )

    def clean(self, value):
        if not value:
            return []
        authors = []
        for item in value:
            author = NameForm(item)
            if not author.is_valid():
                raise ValidationError("Invalid author")
            else:
                authors.append(author.save())
        return authors


class DateField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            queryset=Name.objects.all(),
            required=False,
            **kwargs,
        )

    def clean(self, value):
        if not value:
            return []
        authors = []
        for item in value:
            author = NameForm(item)
            if not author.is_valid():
                raise ValidationError("Invalid author")
            else:
                authors.append(author.save())
        return authors
