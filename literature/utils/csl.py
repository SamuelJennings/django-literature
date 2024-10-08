from django.db import transaction

from ..forms import CSLForm
from ..models import LiteratureItem


def process_single_entry(entry: dict):
    print(entry.get("citation-key"))
    instance = LiteratureItem.objects.filter(citation_key=entry.get("citation-key")).first()
    form = CSLForm(entry, instance=instance)
    if entry.get("citation-key") == "Anderson_1940":
        x = 1
    if form.is_valid():
        form.save()
    else:
        return entry, form.errors


def process_multiple_entries(entries: list):
    with transaction.atomic():
        errors = []
        for entry in entries:
            try:
                result = process_single_entry(entry)
            except Exception as e:
                result = entry, {"non-field-specific": [str(e)]}
            if result:
                errors.append(result)
        return errors
