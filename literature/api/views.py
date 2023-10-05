from rest_framework import viewsets

from ..models import Literature
from .serialize import LiteratureSerializer


class LiteratureViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows literature to be viewed or edited."""

    serializer_class = LiteratureSerializer
    queryset = Literature.objects.all()
