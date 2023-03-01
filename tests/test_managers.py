from pprint import pprint

from django.test import TestCase

from literature.models import Author, Literature


class TestLiteratureManager(TestCase):
    def setUp(self):
        self.doi = "10.1093/gji/ggz376"
        self.manager = Literature.objects

    def test_resolve_for_crossref_doi(self):
        doi = "10.1093/gji/ggz376"
        data, errors = Literature.objects.resolve_doi(doi)

        # pprint(data)
        self.assertTrue("doi" in data.keys())
        self.assertFalse(errors)
        # self.assert
        # self.assertTrue("doi" in data.keys())
