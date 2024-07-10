from django.conf import settings

LITERATURE_STYLES_DIR = "csl_styles"

LITERATURE_DEFAULT_STYLE = "apa"


def get_setting(name):
    name = "LITERATURE_" + name.upper()
    # first check if the setting is in the settings file
    # if not, return the default setting as declared in this file
    return getattr(settings, name, globals()[name])
