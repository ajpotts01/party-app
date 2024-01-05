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
    paginate_by: int = 6  # Even number to match two columns

    def get_queryset(self) -> QuerySet:
        return Party.objects.filter(
            organizer=self.request.user, party_date__gte=dt.datetime.today()
        ).order_by("party_date")

    def get_template_names(self) -> list[str]:
        if "HTTP_HX_REQUEST" in self.request.META:
            return ["party/party_list/partial_parties_list.html"]
        else:
            return ["party/party_list/page_parties_list.html"]
