from django.views.generic import DetailView, ListView

from literature.models import Author, Literature


class CitationMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["citation_style"] = self.citation_style
        return context


class LiteratureList(CitationMixin, ListView):
    model = Literature

    def get_queryset(self):
        return super().get_queryset().prefetch_related("authors")


class LiteratureDetail(CitationMixin, DetailView):
    model = Literature


class AuthorList(ListView):
    model = Author

    def get_queryset(self):
        return super().get_queryset().with_work_counts()


class AuthorDetail(CitationMixin, DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["literature_list"] = context["author"].literature.prefetch_related("authors")
        return context
