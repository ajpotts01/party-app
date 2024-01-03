# Stndard imports
import uuid
from typing import Any

# Third-party imports
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView, ListView

from party.forms import GiftForm
from party.models import Gift, Party


class GiftRegistryPage(ListView):
    model: type = Gift
    template_name: str = "party/gift_registry/page_gift_registry.html"
    context_object_name: str = "gifts"

    def get_queryset(self) -> QuerySet[Gift]:
        return Gift.objects.filter(party_id=self.kwargs["party_uuid"])

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict = super().get_context_data(**kwargs)
        context["party"] = Party.objects.get(uuid=self.kwargs["party_uuid"])
        return context


class GiftDetailPartial(DetailView):
    model: type = Gift
    template_name: str = "party/gift_registry/partial_gift_detail.html"
    context_object_name: str = "gift"
    pk_url_kwarg: str = "gift_uuid"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict = super().get_context_data(**kwargs)
        context["party"] = self.object.party
        return context


class GiftUpdateFormPartial(View):
    def get(
        self, request: HttpRequest, gift_uuid: uuid.UUID, *args, **kwargs
    ) -> HttpResponse:
        gift: Gift = get_object_or_404(klass=Gift, uuid=gift_uuid)
        form: GiftForm = GiftForm(instance=gift)

        return render(
            request=request,
            template_name="party/gift_registry/partial_gift_update.html",
            context={"form": form, "gift": gift},
        )

    def put(
        self, request: HttpRequest, gift_uuid: uuid.UUID, *args, **kwargs
    ) -> HttpResponse:
        data: dict = QueryDict(query_string=request.body).dict()
        gift: Gift = Gift.objects.get(uuid=gift_uuid)
        form: GiftForm = GiftForm(data, instance=gift)

        if form.is_valid():
            form.save()

            return render(
                request=request,
                template_name="party/gift_registry/partial_gift_detail.html",
                context={
                    "gift": gift,
                    "party": gift.party,
                },
            )

        return render(
            request=request,
            template_name="party/gift_registry/partial_gift_update.html",
            context={
                "form": form,
                "gift": gift,
            },
        )
