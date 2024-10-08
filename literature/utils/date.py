def parse_single_date(date_array):
    """Parse a single date-parts array into a dict containing year, month and day."""
    return dict(zip(("year", "month", "day"), date_array))


def date_parts_to_iso(date_parts):
    if not date_parts:
        return None

    if isinstance(date_parts, list):
        date_parts = zip(("year", "month", "day"), date_parts)

    iso = f"{date_parts['year']:04d}"

    if month := date_parts.get("month"):
        iso += f"-{month:02d}"

    if day := date_parts.get("day"):
        iso += f"-{day:02d}"

    return iso


def iso_to_date_parts(iso):
    if not iso:
        return None
    try:
        return [int(part) for part in iso.split("-")]
    except ValueError:
        raise ValueError(f"Encountered invalid date format: {iso}")


def parse_raw_date(date_str):
    """Parse a raw date string into a CSL date-parts array."""
    # raw date string may be one or two partial isodate strings separated by a slash
    # e.g. "2020-01-01/2020-01-31" or "2020-01-01" or "2020-01" or "2020-01/2020-02"
    if not date_str:
        return []
    date_parts = date_str.split("/")
    return [iso_to_date_parts(date) for date in date_parts]


def parse_date_array(date_array):
    """Parse a date-parts array into a CSL date-parts array."""
    return [parse_single_date(date_array)]


def parse_date(json_data):
    # make a copy so we don't modify the original
    result = dict(json_data)
    date_parts = result.get("date-parts", []) or parse_raw_date(result.pop("raw", ""))
    for date_type, part in zip(["begin", "end"], date_parts):
        result[date_type] = parse_single_date(part)

    result["circa"] = bool(result.pop("circa", None))

    return result
