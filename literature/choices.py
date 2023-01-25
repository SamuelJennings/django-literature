from django.db import models
from django.utils.translation import gettext_lazy as _


class MonthChoices(models.IntegerChoices):

    JAN = (
        1,
        _("January"),
    )
    FEB = (
        2,
        _("February"),
    )
    MAR = (
        3,
        _("March"),
    )
    APR = (
        4,
        _("April"),
    )
    MAY = (
        5,
        _("May"),
    )
    JUN = (
        6,
        _("June"),
    )
    JUL = (
        7,
        _("July"),
    )
    AUG = (
        8,
        _("August"),
    )
    SEP = (
        9,
        _("September"),
    )
    OCT = (
        10,
        _("October"),
    )
    NOV = (
        11,
        _("November"),
    )
    DEC = 12, _("December")
