from django.conf import settings

LITERATURE_STYLES_DIR = "csl_styles"

LITERATURE_DEFAULT_STYLE = "apa"

DEFAULTS = {
    "styles_dir": LITERATURE_STYLES_DIR,
    "default_style": LITERATURE_DEFAULT_STYLE,
    "key_generator_func": "shortuuid",
    "preserve_keys_on_import": False,
}


def get_setting(name):
    SETTINGS = DEFAULTS.update(settings.get("REFERENCE_MANAGER", {}))
    # return SETTINGS.get(name)
    name = "LITERATURE_" + name.upper()
    # first check if the setting is in the settings file
    # if not, return the default setting as declared in this file
    return getattr(settings, name, globals()[name])
