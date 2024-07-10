import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

django.setup()

import json

from citeproc.source.json import CiteProcJSON

with open("tests/data/publication-csl.json") as f:
    data = json.load(f)

citeprocjson = CiteProcJSON(data)

reference = citeprocjson.get("test_1")
x = 9
