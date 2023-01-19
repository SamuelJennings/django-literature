from urllib.parse import urlparse


def clean_doi(doi):
    return urlparse(doi).path.strip("/").lower()
