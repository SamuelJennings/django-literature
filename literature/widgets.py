from django.forms.widgets import ChoiceWidget, MultiWidget, TextInput

from .choices import MonthChoices


class DatePartsWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            ChoiceWidget(),
            ChoiceWidget(choices=MonthChoices),
            ChoiceWidget(),
        ]
        super().__init__(widgets, attrs)


class OnlineSearchWidget(TextInput):
    template_name = "literature/widgets/identifier.html"


class PreviewWidget(TextInput):
    template_name = "literature/widgets/preview.html"
