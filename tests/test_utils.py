from datetime import datetime

from django.test import TestCase
from model_bakery import baker

from literature import utils


class TestUtils(TestCase):
    def setUp(self):
        authors = baker.prepare("literature.Author", family="Jennings", _quantity=1)
        self.pub = baker.make(
            "literature.Literature",
            title=(
                "This should be a really long title so we can test whether the uploaded pdf name is shortened properly"
                " using the simple_file_renamer"
            ),
            authors=authors,
            CSL={
                "title": (
                    "This should be a really long title so we can test whether the uploaded pdf name is shortened"
                    " properly using the simple_file_renamer"
                )
            }
            # year=2022,
        )

    def test_clean_doi(self):
        doi = "10.1093/gji/ggz376"
        clean = utils.clean_doi
        self.assertEqual(doi, clean(doi))
        self.assertEqual(doi, clean("doi.org/10.1093/gji/ggz376"))
        self.assertEqual(doi, clean("https://doi.org/10.1093/gji/ggz376"))
        self.assertEqual(doi, clean("http://doi.org/10.1093/gji/ggz376"))
        self.assertEqual(doi, clean("www.doi.org/10.1093/gji/ggz376"))

    # def test_simple_autolabeler(self):
    #     label = utils.simple_autolabeler(self.pub)
    #     self.assertEqual(label, "Jennings2022")
    #     self.pub.citation_key = label
    #     self.pub.save()
    #     new_pub = baker.make(
    #         "literature.Literature",
    #         label="test",
    #         authors=self.pub.authors.all(),
    #         CSL={'title': 'This should be a really long title so we can test whether the uploaded pdf name is shortened properly using the simple_file_renamer'}
    #     )
    #     label = utils.simple_autolabeler(new_pub)
    #     self.assertEqual(label, "Jennings2022b")

    def test_get_current_year(self):
        year = utils.get_current_year()
        self.assertEqual(datetime.now().year, year)

    def test_simple_file_renamer(self):
        new_name = utils.pdf_file_renamer(self.pub)
        self.assertEqual(new_name, "literature/" + self.pub.title[:50].strip() + ".pdf")
        self.assertEqual(len(new_name), 64)
