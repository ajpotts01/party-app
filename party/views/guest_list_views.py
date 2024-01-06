# Standard lib imports
import uuid

# Third-party imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import QueryDict, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

# Project imports
from party.models import Guest


class GuestListPage(LoginRequiredMixin, ListView):
    model: type = Guest
    template_name: str = "party/guest_list/page_guest_list.html"
    context_object_name: str = "guests"

    def get_queryset(self) -> QuerySet[Guest]:
        return Guest.objects.filter(party_id=self.kwargs["party_uuid"])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["party_id"] = self.kwargs["party_uuid"]
        context["attending_num"] = self.object_list.filter(attending=True).count()
        return context


@login_required
@require_http_methods(["PUT"])
def mark_attending_partial(request: HttpRequest, party_uuid: uuid.UUID) -> HttpResponse:
    mark_attending: QueryDict = QueryDict(query_string=request.body).getlist(
        key="guest_ids"
    )
    Guest.objects.filter(uuid__in=mark_attending).update(attending=True)

    guests: QuerySet = Guest.objects.filter(party_id=party_uuid)

    return render(
        request=request,
        template_name="party/guest_list/partial_guest_list.html",
        context={"guests": guests},
    )


@login_required
@require_http_methods(["PUT"])
def mark_not_attending_partial(request: HttpRequest, party_uuid: uuid.UUID):
    mark_not_attending: QueryDict = QueryDict(query_string=request.body).getlist(
        key="guest_ids"
    )
    Guest.objects.filter(uuid__in=mark_not_attending).update(attending=False)

    guests: QuerySet = Guest.objects.filter(party_id=party_uuid)

    return render(
        request=request,
        template_name="party/guest_list/partial_guest_list.html",
        context={"guests": guests},
    )


def filter_attending(party_id: uuid.UUID, **kwargs) -> QuerySet:
    return Guest.objects.filter(party_id=party_id, attending=True)


def filter_not_attending(party_id: uuid.UUID, **kwargs) -> QuerySet:
    return Guest.objects.filter(party_id=party_id, attending=False)


def filter_attending_and_search(party_id: uuid.UUID, **kwargs) -> QuerySet:
    return Guest.objects.filter(
        party_id=party_id, attending=True, name__icontains=kwargs.get("search_text")
    )


def filter_not_attending_and_search(party_id: uuid.UUID, **kwargs) -> QuerySet:
    return Guest.objects.filter(
        party_id=party_id, attending=False, name__icontains=kwargs.get("search_text")
    )


def filter_search(party_id: uuid.UUID, **kwargs) -> QuerySet:
    return Guest.objects.filter(
        party_id=party_id, name__icontains=kwargs.get("search_text")
    )


def filter_default(party_id: uuid.UUID, **kwargs) -> QuerySet:
    return Guest.objects.filter(party_id=party_id)


QUERY_FILTERS = {
    ("attending", False): filter_attending,
    ("not_attending", False): filter_not_attending,
    ("attending", True): filter_attending_and_search,
    ("not_attending", True): filter_not_attending_and_search,
    ("all", True): filter_search,
}


@require_http_methods(["POST"])
def filter_guests_partial(request: HttpRequest, party_uuid: uuid.UUID):
    attending_filter: str = request.POST.get("attending_filter")
    search_text: str = request.POST.get("guest_search")

    query_filter: QuerySet = QUERY_FILTERS.get(
        (attending_filter, bool(search_text)), filter_default
    )

    guests: QuerySet = query_filter(party_id=party_uuid, search_text=search_text)

    return render(
        request=request,
        template_name="party/guest_list/partial_guest_list.html",
        context={"guests": guests},
    )
