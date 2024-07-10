import json

from django.db import models
from django_jsonform.models.fields import JSONField

with open("tests/data/csl-data.json") as f:
    schema = json.load(f)


class Product(models.Model):
    name = models.CharField(max_length=50)

    price = models.DecimalField(max_digits=5, decimal_places=2)

    properties = JSONField(schema=schema)
