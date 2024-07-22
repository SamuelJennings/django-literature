from crispy_forms.layout import HTML, ButtonHolder, Field, Reset, Submit
from django.utils.translation import gettext as _


class HelpText(HTML):
    def __init__(self, html, *args, **kwargs):
        super().__init__(f'<p class="form-text">{html}</p>', *args, **kwargs)


class DateVariable(Field):
    template = "literature/layouts/datevariable.html"

    # def __init__(self, field, **kwargs):
    #     super().__init__(
    #         Field(field, template="literature/layouts/datevariable.html"),
    #     )


BUTTON_HOLDER = ButtonHolder(
    Submit("submit", _("Save")),
    Reset("reset", _("Reset"), css_class="btn btn-outline-secondary ms-2"),
    HTML(
        '{{% if object.pk %}}<a href="{{% url "literature-delete" pk=object.pk %}}" class="btn btn-danger ms-auto">{}</a>{{% endif %}}'.format(
            _("Delete")
        )
    ),
    css_class="sticky-bottom mb-3 d-flex w-100 border-top bg-white py-1",
)
