import re

CSL_STYLES_URL = "https://cdn.jsdelivr.net/gh/citation-style-language/styles@master/{style_template}.csl"


def normalize_doi(doi):
    """
    Normalize any DOI input to a full https://doi.org/ URL.

    Examples:
        - "10.1000/xyz123" → "https://doi.org/10.1000/xyz123"
        - "doi:10.1000/xyz123" → "https://doi.org/10.1000/xyz123"
        - "https://doi.org/10.1000/xyz123" → "https://doi.org/10.1000/xyz123"

    Returns None if input does not look like a valid DOI.
    """
    if not doi:
        return None

    # Strip whitespace and lowercase DOI scheme
    doi = doi.strip()

    # Remove common prefixes
    doi = re.sub(r"^(doi:|DOI:|https?://(dx\.)?doi\.org/)", "", doi, flags=re.IGNORECASE)

    # Check for valid DOI pattern
    if not re.match(r"^10\.\d{4,9}/\S+$", doi):
        return None

    return f"https://doi.org/{doi}"
