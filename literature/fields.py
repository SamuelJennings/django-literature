from django import forms

from .choices import MonthChoices


class DateInput(forms.MultiWidget):
    template_name = "widgets/multiwidget.html"

    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(attrs={"class": "form-control"}),
            forms.Select(choices=MonthChoices.choices, attrs={"class": "form-control"}),
            forms.NumberInput(attrs={"class": "form-control"}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.day, value.month, value.year]
        return [None, None, None]


class DateField(forms.MultiValueField):
    widget = DateInput

    def __init__(self, **kwargs):
        kwargs["fields"] = (
            forms.IntegerField(min_value=1, max_value=31),
            forms.IntegerField(min_value=1, max_value=12),
            forms.IntegerField(min_value=1000, max_value=9999),
        )
        kwargs["require_all_fields"] = False
        # kwargs["widget"] = DateInput(attrs=kwargs.get("attrs", None))
        super().__init__(**kwargs)

    def compress(self, data_list):
        if data_list:
            return data_list
            # return date(day=data_list[0], month=data_list[1], year=data_list[2])
        return None
