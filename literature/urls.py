from django.urls import path

from . import views

app_name = "literature"
urlpatterns = [
    path("", views.LiteratureList.as_view(), name="list"),
    path("<pk>/", views.LiteratureDetail.as_view(), name="detail"),
]
