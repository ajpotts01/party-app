# Standard lib imports
import datetime as dt

# Third-party imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import ListView

# Project imports
from party.models import Party


class PartyListPage(LoginRequiredMixin, ListView):
    template_name: str = "party/party_list/page_parties_list.html"
    context_object_name: str = "parties"

    def get_queryset(self) -> QuerySet:
        return Party.objects.filter(
            organizer=self.request.user, party_date__gte=dt.datetime.today()
        ).order_by("party_date")
