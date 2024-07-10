from django.template import Engine
from django.template.loaders.filesystem import Loader
from django.template.utils import get_app_template_dirs


class CustomAppDirectoriesLoader(Loader):
    def get_dirs(self):
        # return [get_setting("STYLES_DIR"), *list(get_app_template_dirs("csl_styles"))]
        return get_app_template_dirs("csl_styles")

    def get_contents(self, origin):
        return origin.name


style_loader = Engine(
    loaders=[
        ("literature.loaders.CustomAppDirectoriesLoader", ()),
    ]
)

style_loader.get_style_path = style_loader.get_template
