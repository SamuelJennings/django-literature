from datetime import date

from dateutil.relativedelta import relativedelta
from django.db.models import Count, Max, Q
from django.db.models.query import QuerySet
from django.utils.module_loading import import_string

from literature.conf import settings

from .exceptions import AdaptorError, RemoteAdaptorError


class AuthorQuerySet(QuerySet):
    def with_work_counts(self):
        """Convenience filter for retrieving authors with annotated
        counts of works published as either lead or supporting author.

        These count attributes can be accessed on the queryset as
        `as_lead` or `as_supporting`. Further filtering/manipulation is
        possible on both fields afterwards.

        Example:
            Get authors that have published at least five works as
            lead author.

            >>> Author.objects.with_work_counts().filter(as_lead__gte=5)

            Get authors that have published only once but have been a supporting
            author on at least three.

            >>> Author.objects.with_work_counts().filter(as_lead=1, as_supporting__gte=3)
        """
        return self.prefetch_related("literature").annotate(
            as_lead=Count("position", filter=Q(position__position=1)),
            as_supporting=Count("position", filter=Q(position__position__gt=1)),
        )

    def as_lead(self):
        """Convenience filter for retrieving only authors that
        are listed as the lead author on a publication."""

        return (
            self.prefetch_related("literature")
            .annotate(as_lead=Count("position", filter=Q(position__position=1)))
            .filter(as_lead__gt=0)
        )

    def with_last_published(self):
        return self.prefetch_related("literature").annotate(last_published=Max("literature__published"))

    def is_active(self):
        cutoff = date.today() - relativedelta(years=settings.LITERATURE_INACTIVE_AFTER)
        return self.with_last_published().filter(last_published__gt=cutoff)


AuthorManager = AuthorQuerySet.as_manager


class LiteratureQuerySet(QuerySet):
    def resolve_doi(self, doi, adaptor=None):
        """Attempts to fetch a doi from a remote data source. Loops through the
        available remote adaptors until the doi is succesfully resolved. If the doi
        registrar (source) is known, you may supply the appropriate adaptor to prevent
        searching other registries.

        Args:
            doi (_type_): _description_
            adaptor (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        adaptors = [adaptor] if adaptor else [import_string(ac) for ac in settings.LITERATURE_ADAPTORS]

        for adaptor in adaptors:
            try:
                return adaptor(doi=doi).get_data()
            except AdaptorError:
                # raised if the adaptor is not remote
                pass
            except RemoteAdaptorError:
                # raised if the adaptor returns a 404
                pass

    def get_or_resolve(self, doi):
        """Loops through all available remote adaptors and attempts to resolve the given DOI until succesful.

        Args:
            doi (_type_): _description_
        """
        try:
            return self.get(doi=doi), False
        except self.model.DoesNotExist:
            for adaptor_class in settings.LITERATURE_ADAPTORS:
                if adaptor_class.is_remote:
                    obj, created = self.resolve_doi_for_adaptor(doi, adaptor_class)

    # def _resolve_doi(self, doi, adaptor):
    #     """
    #     For a given adaptor, attempt to resolve a doi by querying the remote data source.
    #     """
    #     # if not adaptor.is_remote:
    #     # raise AdaptorError(_(f"{adaptor} cannot resolve remote sources."))

    #     # initialize the adaptor with the given doi in an attempt to
    #     # fetch data from the adaptor's API
    #     return adaptor(doi=doi).get_data()

    # async def aresolve_doi_for_adaptor(self, doi):
    #     return await sync_to_async(self.resolve_doi_for_adaptor)(doi)


LiteratureManager = LiteratureQuerySet.as_manager
