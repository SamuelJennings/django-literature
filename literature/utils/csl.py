from ..forms import CSLForm


def process_single_entry(entry: dict):
    form = CSLForm(entry)
    if form.is_valid():
        form.save()
    else:
        return entry, form.errors


def process_multiple_entries(entries: list):
    errors = []
    for entry in entries:
        result = process_single_entry(entry)
        if result:
            errors.append(result)
    return errors
