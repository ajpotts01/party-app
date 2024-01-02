# Standard lib imports
import uuid

# Third-party imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView

# Project imports
from party.forms import PartyForm
from party.models import Party

class PartyDetailPage(LoginRequiredMixin, DetailView):
    model: type = Party
    template_name: str = "party/party_detail/page_party_detail.html"
    pk_url_kwarg: str = "party_uuid"
    context_object_name: str = "party"


class PartyDetailPartial(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, party_uuid: uuid.UUID, *args, **kwargs) -> HttpResponse:
        party: Party = get_object_or_404(klass=Party, uuid=party_uuid)
        form: PartyForm = PartyForm(instance=party)

        return render(request=request,
                      template_name="party/party_detail/partial_party_edit_form.html",
                      context={
                          "party": party,
                          "form": form,
                      },
        )
    
    def put(self, request: HttpResponse, party_uuid: uuid.UUID, *args, **kwargs) -> HttpResponse:
        party: Party = get_object_or_404(klass=Party, uuid=party_uuid)
        data: QueryDict = QueryDict(query_string=request.body).dict()
        form: PartyForm = PartyForm(data=data, instance=party)

        if form.is_valid():
            form.save()

        return render(request=request, 
                      template_name="party/party_detail/partial_party_detail.html",
                      context={
                          "party": party,
                      },
                    )