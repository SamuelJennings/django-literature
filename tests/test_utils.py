import json

import pytest

from literature.utils import csl_to_django_lit, django_lit_to_csl

# normal dict
d1 = {"key-1": "x", "key-2": "y"}
d1_expected = {"key_1": "x", "key_2": "y"}

# nested dict
d2 = {"key-1": {"nested-key-1": "nested-value-1"}, "key-2": "value-2"}
d2_expected = {"key_1": {"nested_key_1": "nested-value-1"}, "key_2": "value-2"}

# list
d3 = ["value-1", "value-2"]
d3_expected = ["value-1", "value-2"]

# mixed data types
d4 = {"key-1": ["value-1", "value-2"], "key-2": {"nested-key-1": "nested-value-1"}}
d4_expected = {"key_1": ["value-1", "value-2"], "key_2": {"nested_key_1": "nested-value-1"}}


@pytest.mark.parametrize(
    "input_dict, expected_output_dict",
    [
        (d1, d1_expected),
        (d2, d2_expected),
        (d3, d3_expected),
        (d4, d4_expected),
    ],
)
def test_csl_to_django_lit(input_dict, expected_output_dict):
    assert csl_to_django_lit(input_dict) == expected_output_dict


def test_csljson_to_dict():
    with open("tests/data/publication-csl.json") as f:
        csljson = json.load(f)

    output = csl_to_django_lit(csljson[0])
    assert "container_title" in output
    assert "container-title" not in output

    # # test nested lists
    # author = output["author"][0]
    # assert "authenticated_orcid" in author
    # assert "authenticated-orcid" not in author

    # test nested dicts
    issued = output["issued"]
    assert "date_parts" in issued
    assert "date-parts" not in issued


def test_django_lit_to_csl():
    with open("tests/data/publication-csl.json") as f:
        csljson = json.load(f)

    output = csl_to_django_lit(csljson[0])

    original = django_lit_to_csl(output)

    assert original == csljson[0]
