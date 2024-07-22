from django import template
from django.db.models import QuerySet

register = template.Library()


def bibliography(objs: list | QuerySet, style=""):
    """Renders a bibligraphy for a queryset of LiteratureItem objects."""
    pass


@register.simple_tag
def cite(*args):
    """In-text citation analagous to LaTex cite command.

    *args: any number of citation labels that match an object in the database
    """

    labels = list(args)

    qs = LiteratureItem.objects.filter(label__in=labels)


@register.simple_tag
def citep(objs: list | QuerySet, style=""):
    """Paranthetical citation analagous to LaTex citep command"""
    pass
