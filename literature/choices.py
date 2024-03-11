from django.db import models
from django.utils.translation import gettext as _

CSL_TYPE_CHOICES = [
    ("article", _("Article (Generic)")),
    ("article-journal", _("Article (Journal)")),
    ("article-magazine", _("Article (Magazine)")),
    ("article-newspaper", _("Article (Newspaper)")),
    ("bill", _("Legislative bill")),
    ("book", _("Book")),
    ("broadcast", _("Broadcast")),
    ("chapter", _("Book chapter")),
    ("classic", _("Classic work")),
    ("collection", _("Collection of works")),
    ("dataset", _("Dataset")),
    ("document", _("Document (Generic)")),
    ("entry", _("Entry (Generic)")),
    ("entry-dictionary", _("Entry (Dictionary)")),
    ("entry-encyclopedia", _("Entry (Encyclopedia)")),
    ("event", _("Event")),
    ("figure", _("Figure or illustration")),
    ("graphic", _("Graphic work")),
    ("hearing", _("Congressional hearing")),
    ("interview", _("Interview")),
    ("legal_case", _("Legal case")),
    ("legislation", _("Legislation")),
    ("manuscript", _("Manuscript")),
    ("map", _("Map")),
    ("motion_picture", _("Motion picture")),
    ("musical_score", _("Musical score")),
    ("pamphlet", _("Pamphlet")),
    ("paper-conference", _("Conference paper")),
    ("patent", _("Patent")),
    ("performance", _("Live performance")),
    ("periodical", _("Generic periodical")),
    ("personal_communication", _("Personal communication")),
    ("post", _("Blog post")),
    ("post-weblog", _("Weblog post")),
    ("regulation", _("Regulation")),
    ("report", _("Report")),
    ("review", _("Review")),
    ("review-book", _("Book review")),
    ("software", _("Software")),
    ("song", _("Song")),
    ("speech", _("Speech")),
    ("standard", _("Standard")),
    ("thesis", _("Thesis")),
    ("treaty", _("Treaty")),
    ("webpage", _("Webpage")),
]

# These fields are explicitly shown in the form when the given type is selected by the user.
# If a field does not appear in any list, it will be shown for all types.
CSL_SUGGESTED_PROPERTIES = {
    "article": [
        "author",
        "title",
        "title-short",
        "container-title",
        "container-title-short",
        "issue",
        "number",
        "page",
        "publisherpublisher-place",
        "edition",
        "issued",
        "collection-number",
        "collection-title",
        "section",
        "status",
        "supplement-number",
        "volume",
        "volume-title",
    ],
    "article-journal": [
        "author",
        "title",
        "container-title",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "article-magazine": [
        "author",
        "title",
        "container-title",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "article-newspaper": [
        "author",
        "title",
        "container-title",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "bill": [
        "title",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "book": [
        "author",
        "collection_editor",
        "title",
        "publisher",
        "publisher-place",
        "volume",
        "edition",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "broadcast": [
        "title",
        "event-date",
        "medium",
        "URL",
    ],
    "chapter": [
        "author",
        "title",
        "container-title",
        "volume",
        "page",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "classic": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "volume",
        "edition",
        "issued",
        "ISBN",
        "URL",
    ],
    "collection": [
        "editor",
        "collection_editor",
        "title",
        "publisher",
        "publisher-place",
        "volume",
        "edition",
        "issued",
        "ISBN",
        "URL",
    ],
    "dataset": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "issued",
        "URL",
        "compiler",
        "license",
    ],
    "document": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "license",
        "URL",
    ],
    "entry": [
        "title",
        "container-title",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "entry-dictionary": [
        "title",
        "container-title",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "entry-encyclopedia": [
        "title",
        "container-title",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "event": [
        # "title",
        "event",
        "event-place",
        "event-title",
        "event-date",
        "chair",
        "URL",
    ],
    "figure": [
        "title",
        "creator",
        "dimensions",
        "URL",
    ],
    "graphic": [
        "title",
        "creator",
        "illustrator",
        "dimensions",
        "URL",
    ],
    "hearing": [
        "title",
        "event-date",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "interview": [
        "interviewer",
        "title",
        "container-title",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "legal_case": [
        "title",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "legislation": [
        "title",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "manuscript": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "map": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "issued",
        "scale",
        "ISBN",
        "DOI",
        "URL",
    ],
    "motion_picture": [
        "director",
        "executive-producer",
        "title",
        "container-title",
        "guest",
        "host",
        "narrator",
        "volume",
        "page",
        "issued",
        "medium",
        "DOI",
        "URL",
    ],
    "musical_score": [
        "author",
        "composer",
        "title",
        "publisher",
        "publisher-place",
        "volume",
        "edition",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "pamphlet": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "volume",
        "edition",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "paper-conference": [
        "author",
        "title",
        "container-title",
        "event-date",
        "page",
        "publisher",
        "publisher-place",
        "issued",
        "DOI",
        "URL",
    ],
    "patent": [
        "title",
        "authority",
        "URL",
    ],
    "performance": [
        "performer",
        "title",
        "event-date",
        "medium",
        "URL",
    ],
    "periodical": [
        "editor",
        "title",
        "container-title",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "personal_communication": [
        "author",
        "title",
        "URL",
    ],
    "post": [
        "author",
        "title",
        "container-title",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "post-weblog": [
        "author",
        "title",
        "container-title",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "regulation": [
        "title",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "report": [
        "author",
        "title",
        "institution",
        "URL",
    ],
    "review": [
        "author",
        "title",
        "reviewed-title",
        "reviewed-genre",
        "container-title",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "review-book": [
        "author",
        "title",
        "container-title",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "software": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "version",
        "license",
        "URL",
    ],
    "song": [
        "author",
        "title",
        "container-title",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "speech": [
        "author",
        "title",
        "event-date",
        "medium",
        "URL",
    ],
    "standard": [
        "authority",
        "title",
        "URL",
    ],
    "thesis": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "treaty": [
        "title",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "webpage": [
        "author",
        "title",
        "container-title",
        "page",
        "issued",
        "URL",
    ],
}


CSL_ALWAYS_SHOW = [
    "abstract",
    "archive",
    "archive_location",
    "archive-place",
    "archive-collection",
    "keyword",
    "language",
    "note",
    "annote",
    "source",
    "PMCID",
    "PMID",
    "DOI",
    "ISBN",
    "ISSN",
    "URL",
]


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


class TypeChoices(models.TextChoices):
    article = "article", _("article")
    article_journal = "article-journal", _("journal article")
    article_magazine = "article-magazine", _("magazine article")
    article_newspaper = "article-newspaper", _("newspaper article")
    bill = "bill", _("bill")
    book = "book", _("book")
    broadcast = "broadcast", _("broadcast")
    chapter = "chapter", _("chapter")
    dataset = "dataset", _("dataset")
    entry = "entry", _("entry")
    entry_dictionary = "entry-dictionary", _("entry (dictionary)")
    entry_encyclopedia = "entry-encyclopedia", _("entry (encyclopedia)")
    figure = "figure", _("figure")
    graphic = "graphic", _("graphic")
    interview = "interview", _("interview")
    legal_case = "legal_case", _("legal case")
    legislation = "legislation", _("legislation")
    manuscript = "manuscript", _("manuscript")
    map = "map", _("map")
    motion_picture = "motion_picture", _("motion picture")
    musical_score = "musical_score", _("musical score")
    pamphlet = "pamphlet", _("pamphlet")
    paper_conference = "paper-conference", _("paper conference")
    patent = "patent", _("patent")
    personal_communication = "personal_communication", _("personal communication")
    post = "post", _("post")
    post_weblog = "post-weblog", _("blog post")
    report = "report", _("report")
    review = "review", _("review")
    review_book = "review-book", _("review book")
    song = "song", _("song")
    speech = "speech", _("speech")
    thesis = "thesis", _("thesis")
    treaty = "treaty", _("treaty")
    webpage = "webpage", _("webpage")
