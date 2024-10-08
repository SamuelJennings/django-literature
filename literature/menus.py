from django.utils.translation import gettext as _
from flex_menu import Menu, MenuItem

LiteratureMenu = Menu(
    "LiteratureMenu",
    root_template="literature/menus/root.html",
    template="literature/menus/item.html",
    children=[
        Menu(
            _("file"),
            icon="file",
            children=[
                Menu(
                    _("new"),
                    icon="plus",
                    children=[
                        MenuItem(
                            _("item"),
                            view_name="literature-create",
                            icon="plus",
                        ),
                        MenuItem(
                            _("collection"),
                            view_name="literature-create",
                            icon="plus",
                        ),
                    ],
                ),
            ],
        ),
        MenuItem(
            _("import"),
            view_name="literature-import",
            icon="import",
        ),
    ],
)
