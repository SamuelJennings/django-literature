from django.core.exceptions import ValidationError
from django.test import TestCase

from literature.fields import CSLDateField


class CSLDateFieldTestCase(TestCase):
    def test_to_python_valid_json(self):
        field = CSLDateField()
        # value = '[{"date-parts": [[2022, 1, 1]]}, {"literal": "Today"},{"date-parts": [[2022, 1, 1], [2023, 2, 1]]}]'
        value = '{"date-parts": [[2022, 1, 1], [2023, 2]], "circa": 1}'
        expected_output = [
            {"circa": 0, "year": 2022, "month": 1, "day": 1},
            {"text": "Today", "circa": False},
        ]
        output = field.to_python(value)
        self.assertEqual(output, expected_output)

    def test_to_python_invalid_json(self):
        field = CSLDateField()
        value = "invalid json"
        with self.assertRaises(ValidationError) as cm:
            field.to_python(value)
        self.assertEqual(str(cm.exception), "Invalid JSON data")

    def test_validate_missing_field(self):
        field = CSLDateField(model="MyModel", fields=["field1", "field2"])
        value = [
            {"date-parts": [[2022, 1, 1]], "field1": "value1"},
            {"date-parts": [[2022, 1, 2]]},
        ]
        with self.assertRaises(ValidationError) as cm:
            field.validate(value)
        self.assertEqual(str(cm.exception), "Missing field field2 in item {'date-parts': [[2022, 1, 2]]}")
