from django import forms
from django.contrib.auth import get_user_model
from django.forms import fields
from entangled.forms import EntangledModelForm, EntangledModelFormMixin

from .models import Product


class ProductForm(EntangledModelForm):
    color = fields.RegexField(
        regex=r"^#[0-9a-f]{6}$",
    )

    size = fields.ChoiceField(
        choices=[("s", "small"), ("m", "medium"), ("l", "large"), ("xl", "extra large")],
    )

    class Meta:
        model = Product
        entangled_fields = {"properties": ["color", "size"]}  # fields provided by this form
        untangled_fields = ["name", "price"]  # these fields are provided by the Product mode

    def save(self, commit):
        return super().save(commit)


class BaseProductForm(EntangledModelFormMixin, forms.ModelForm):
    tenant = forms.ModelChoiceField(
        queryset=get_user_model().objects.filter(is_staff=True),
    )

    class Meta:
        model = Product
        entangled_fields = {"properties": ["tenant"]}
        untangled_fields = ["name", "price"]


class ClothingProductForm(BaseProductForm):
    color = fields.RegexField(
        regex=r"^#[0-9a-f]{6}$",
    )

    size = fields.ChoiceField(
        choices=[("s", "small"), ("m", "medium"), ("l", "large"), ("xl", "extra large")],
    )

    class Meta:
        model = Product
        entangled_fields = {"properties": ["color", "size"]}
        retangled_fields = {"color": "variants.color", "size": "variants.size"}
        untangled_fields = ["name", "price"]

    def save(self, commit):
        return super().save(commit)
