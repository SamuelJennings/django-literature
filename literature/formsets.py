from citeproc.source.bibtex.bibtex import parse_latex, parse_name
from django import forms
from formset.collection import FormCollection
from formset.renderers import bootstrap

from .models import Date


class DateForm(forms.ModelForm):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Date
        fields = ["id", "begin", "end"]

    def clean(self):
        cleaned = super().clean()

        return cleaned


class DateCollection(FormCollection):
    extra_siblings = 0
    legend = "Dates"
    add_label = "Add Date"
    related_field = "item"

    date = DateForm()
    default_renderer = bootstrap.FormRenderer(
        control_css_classes="row",
        form_css_classes="row",
        field_css_classes={
            "family": "col-2",
            "given": "col-2",
            "suffix": "col-1",
        },
    )

    def retrieve_instance(self, data):
        if data := data.get("date"):
            try:
                return self.instance.dates.get(id=data.get("id") or 0)
            except (AttributeError, Date.DoesNotExist, ValueError):
                return Date(name=data.get("name"), department=self.instance)

    def clean(self):
        cleaned = super().clean()
        first, von, last, jr = parse_name(cleaned["name"])
        csl_parts = {}
        for part, csl_label in [(first, "given"), (von, "non-dropping-particle"), (last, "family"), (jr, "suffix")]:
            if part is not None:
                csl_parts[csl_label] = parse_latex(part, {})
        name, created = Date.objects.get_or_create(**csl_parts)

        return cleaned


class LiteratureForm(FormCollection):
    dates = DateCollection()
