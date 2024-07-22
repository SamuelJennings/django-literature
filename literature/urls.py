from django.urls import path

from .views import ImportView, LiteratureCreateView, LiteratureView

# app_name = "literature"
urlpatterns = [
    path("import/", ImportView.as_view(), name="import"),
    *LiteratureView.get_urls(),
    path("literature/create/", LiteratureCreateView.as_view(), name="literature-create"),
    # path("literature/<pk>/formset/", LiteratureEditView.as_view(), name="literature-edit"),
]

for p in urlpatterns:
    print(p)
