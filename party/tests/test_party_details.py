# Standard lib imports
import datetime as dt
from typing import Callable
from urllib.parse import urlencode

# Third-party imports
import pytest
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

# Project imports
from party.models import Party


@pytest.mark.django_db
def test_party_detail_page_returns_whole_page_with_single_party(
    authenticated_client: Client,
    create_user: Callable,
    django_user_model: User,
    create_party: Callable,
):
    party: Party = create_party(organizer=create_user)
    url: str = reverse(viewname="page_single_party", args=[party.uuid])
    response: HttpResponse = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert response.context_data["party"] == party

@pytest.mark.django_db
def test_party_detail_partial_get_method_returns_a_form_prefilled_with_party_details(
    authenticated_client: Client, 
    create_user: Callable, 
    create_party: Callable,
):
    party: Party = create_party(organizer=create_user)

    url: str = reverse(viewname="partial_party_detail", args=[party.uuid])
    response: HttpResponse = authenticated_client(create_user).get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].instance == party

@pytest.mark.django_db
def test_party_detail_partial_put_method_returns_updated_party_details(
    authenticated_client: Client, 
    create_user: Callable, 
    create_party: Callable
):
    party: Party = create_party(organizer=create_user)

    url: str = reverse(viewname="partial_party_detail", args=[party.uuid])

    data: str = urlencode(
        {
            "party_date": "2025-06-06",
            "party_time": "18:00:00",
            "venue": "New Venue",
            "invitation": "New Bla bla",
        }
    )

    response: HttpResponse = authenticated_client(create_user).put(url, content_type="application/json", data=data)

    assert response.status_code == 200
    assert Party.objects.get(uuid=party.uuid).party_date == dt.date(2025, 6, 6)
    assert Party.objects.get(uuid=party.uuid).party_time == dt.time(18, 0)
    assert Party.objects.get(uuid=party.uuid).venue == "New Venue"
    assert Party.objects.get(uuid=party.uuid).invitation == "New Bla bla"