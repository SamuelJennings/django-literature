from django.urls import path

from .views import ProductEditView

urlpatterns = [
    path("<pk>/", ProductEditView.as_view(), name="index"),
]
