# Standard lib imports
from typing import Callable
from urllib.parse import urlencode

# Third-party imports
import pytest
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

# Project imports
from party.models import Gift, Party


@pytest.mark.django_db
def test_gift_registry_page_lists_gifts_for_party_by_id(
    authenticated_client: Client,
    create_user: Callable,
    create_party: Callable,
    create_gift: Callable,
):
    party: Party = create_party(organizer=create_user, venue="Best venue")
    gift_1: Gift = create_gift(gift="Roses", party=party)
    gift_2: Gift = create_gift(gift="Chocolate", party=party)

    another_party: Party = create_party(organizer=create_user, venue="Another venue")
    create_gift(party=another_party)

    url: str = reverse(viewname="page_gift_registry", args=[party.uuid])
    response: HttpResponse = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert list(response.context_data["gifts"]) == [gift_1, gift_2]


def test_gift_detail_partial_returns_gift_detail_including_party(
    authenticated_client: Client,
    create_user: Callable,
    django_user_model: User,
    create_party: Callable,
    create_gift: Callable,
):
    party: Party = create_party(organizer=create_user)
    gift: Gift = create_gift(party=party)

    url: str = reverse(viewname="partial_gift_detail", args=[gift.uuid])
    response: HttpResponse = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert response.context_data["gift"] == gift
    assert response.context_data["party"] == party


def test_partial_gift_update_returns_gift_update_form(
    authenticated_client: Client,
    create_user: Callable,
    create_party: Callable,
    create_gift: Callable,
):
    party: Party = create_party(create_user)
    gift: Gift = create_gift(party=party)

    url: str = reverse(viewname="partial_gift_update", args=[gift.uuid])
    response: HttpResponse = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].instance == gift


def test_partial_gift_update_updates_gift_and_returns_its_details_including_party_id(
    authenticated_client: Client,
    create_user: Client,
    create_party: Client,
    create_gift: Client,
):
    party: Party = create_party(create_user)
    gift: Gift = create_gift(party=party)

    data: dict = urlencode(
        {
            "gift": "Updated gift",
            "price": "50",
            "link": "https://updatedtestlink.com",
        }
    )

    url = reverse(viewname="partial_gift_update", args=[gift.uuid])
    response = authenticated_client(create_user).put(
        url, content_type="application/json", data=data
    )

    assert Gift.objects.get(uuid=gift.uuid).gift == "Updated gift"
    assert Gift.objects.get(uuid=gift.uuid).price == 50.0
    assert Gift.objects.get(uuid=gift.uuid).link == "https://updatedtestlink.com"

    assert response.status_code == 200
    assert response.context["gift"].gift == "Updated gift"
    assert response.context["party"] == party
