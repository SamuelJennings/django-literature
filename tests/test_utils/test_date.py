import pytest

from literature.utils import date


@pytest.mark.parametrize(
    "array, output",
    [
        ([2014], {"year": 2014}),
        ([2014, 1], {"year": 2014, "month": 1}),
        ([2014, 1, 1], {"year": 2014, "month": 1, "day": 1}),
    ],
)
def test_parse_single_date(array, output):
    assert date.parse_single_date(array) == output


@pytest.mark.parametrize(
    "array, output",
    [
        ([2014], "2014"),
        ([2014, 1], "2014-01"),
        ([2014, 1, 1], "2014-01-01"),
    ],
)
def test_date_parts_to_iso(array, output):
    assert date.date_parts_to_iso(array) == output


@pytest.mark.parametrize(
    "date_str, output",
    [
        ("2014", [2014]),
        ("2014-01", [2014, 1]),
        ("2014-01-01", [2014, 1, 1]),
    ],
)
def test_iso_to_date_parts(date_str, output):
    assert date.iso_to_date_parts(date_str) == output


@pytest.mark.parametrize(
    "date_str, output",
    [
        ("2014/2016", [[2014], [2016]]),
        ("2014-01/2016-01", [[2014, 1], [2016, 1]]),
        ("2014-01-01/2016-01-01", [[2014, 1, 1], [2016, 1, 1]]),
    ],
)
def test_parse_raw_date(date_str, output):
    assert date.parse_raw_date(date_str) == output
