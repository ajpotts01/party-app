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
