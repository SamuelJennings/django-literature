from datetime import date

from asgiref.sync import sync_to_async
from dateutil.relativedelta import relativedelta
from django.conf import settings

# from .adaptors.base import AdaptorError, RemoteAdaptorError
from django.db import transaction
from django.db.models import Count, Max, Q
from django.db.models.query import QuerySet


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
        return self.prefetch_related("works").annotate(
            as_lead=Count("position", filter=Q(position__number=1)),
            as_supporting=Count("position", filter=Q(position__number__gt=1)),
        )

    def as_lead(self):
        """Convenience filter for retrieving only authors that
        are listed as the lead author on a publication."""

        return (
            self.prefetch_related("works")
            .annotate(as_lead=Count("position", filter=Q(position__number=1)))
            .filter(as_lead__gt=0)
        )

    def with_last_published(self):
        return self.prefetch_related("works").annotate(
            last_published=Max("works__published")
        )

    def is_active(self):
        cutoff = date.today() - relativedelta(years=settings.LITERATURE_INACTIVE_AFTER)
        return self.with_last_published().filter(last_published__gt=cutoff)


class WorkQuerySet(QuerySet):
    def get_or_resolve(self, doi):
        """Loops through all available remote adaptors and attempts to resolve the
        given DOI until succesful.

        Args:
            doi (_type_): _description_
        """
        try:
            return self.get(doi=doi), False
        except self.model.DoesNotExist:
            for adaptor_class in getattr(settings, "LITERATURE_ADAPTORS"):
                if adaptor_class.is_remote:
                    obj, created = self.resolve_for_adaptor(doi, adaptor_class)

    def resolve_for_adaptor(self, doi, adaptor_class):
        """
        Look up an object with the given kwargs, fetching one from the
        available adaptors if necessary. Return a tuple of
        (object, created), where created is a boolean specifying whether
        an object was created.
        """
        if not adaptor_class.is_remote:
            raise AdaptorError("The given adaptor cannot resolve remote sources.")

        # initialize the adaptor with the given doi in an attempt to
        # fetch data from the adaptor's API
        adaptor = adaptor_class(doi)

        try:
            with transaction.atomic(using=self.db):
                return adaptor.save(), True
        except IntegrityError:
            try:
                return self.get(**kwargs), False
            except self.model.DoesNotExist:
                pass
            raise

    async def aresolve_for_adaptor(self, doi):
        return await sync_to_async(self.resolve_for_adaptor)(doi)
