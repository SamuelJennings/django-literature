import django_filters
from crispy_forms.helper import FormHelper
from django_filters import FilterSet

from .models import LiteratureItem


class LiteratureSimpleFilter(FilterSet):
    q = django_filters.CharFilter(field_name="item", lookup_expr="icontains")

    class Meta:
        model = LiteratureItem
        fields = ["q"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = "get"
        self.form.helper.form_class = "form-inline"
        self.form.helper.form_show_labels = False

        self.form.fields["q"].widget.attrs["placeholder"] = "Search"
