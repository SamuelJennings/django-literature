import json

import pytest
from citeproc.source.json import CiteProcJSON
from django.test import TestCase
from partial_date import PartialDate

from literature.forms import CSLForm


class CSLFormTestCase(TestCase):
    def setUp(self):
        with open("tests/data/publication-csl.json") as f:
            self.csl_json = json.load(f)[0]

    def test_to_python_valid_json(self):
        form_class = CSLForm
        form = form_class(data=self.csl_json)

        self.assertTrue(form.is_valid())

        x = 8


def parse_date(date_obj):
    def get_date_str(date_obj):
        if not date_obj.get("year"):
            return ""

        date_str = f'{date_obj["year"]}'
        if date_obj.get("month"):
            date_str += f"-{date_obj['month']}"
            if date_obj.get("day"):
                date_str += f"-{date_obj['day']}"
        return date_str

    date = CiteProcJSON.parse_date(None, date_obj)

    if "begin" in date:
        date_str = get_date_str(date["begin"])
        date["begin"] = PartialDate(date_str)

    if "end" in date:
        date_str = get_date_str(date["end"])
        date["end"] = PartialDate(date_str)

    if "year" in date:
        # dealing with a single date
        date_str = get_date_str(date)
        date["begin"] = PartialDate(date_str)
        date.pop("year")
        if "month" in date:
            date.pop("month")
        if "day" in date:
            date.pop("day")
    # if "season" in date:
    #     date[""] = PartialDate(date["season"])

    if "circa" in date:
        date["circa"] = bool(date["circa"])

    if "text" in date:
        # attempting to parse a literal date
        date["begin"] = date["text"]

    return date


@pytest.mark.parametrize(
    "date_obj",
    [
        {"date-parts": [[2023, 6, 27]]},  # single date
        {"date-parts": [[2023, 6]]},  # year and month
        {"date-parts": [[2023]]},  # year only
        {"date-parts": [[2023, 6, 1], [2023, 6, 27]]},  # date range
        {"season": 1, "date-parts": [[2023]]},  # season
        {"season": "Spring", "date-parts": [[2023]]},  # season
        {"circa": True, "date-parts": [[2023]]},  # circa date
        {"literal": "June 27, 2023"},  # literal date
        {"raw": "2023-06-27"},  # raw date
        {"raw": "2023-06-21/2023-06-27"},  # raw date range
    ],
)
def test_parse_date_types(date_obj):
    date = parse_date(date_obj)
    # date = CiteProcJSON.parse_date(None, date_obj)

    x = 8
