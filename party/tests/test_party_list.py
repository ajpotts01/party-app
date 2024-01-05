# Standard lib imports
import datetime as dt
from typing import Callable

# Third-party imports
import pytest
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

# Project imports
from party.models import Party
from party.views import PartyListPage


@pytest.mark.django_db
def test_party_list_page_returns_list_of_users_future_parties(
    authenticated_client: Client,
    create_user: Callable,
    create_party: Callable,
    django_user_model: User,
):
    today: dt.date = dt.date.today()
    user: User = create_user
    other_user: User = django_user_model.objects.create_user(
        username="other_user", password="whatever"
    )

    valid_party_1: Party = create_party(
        organizer=user, party_date=today, venue="Venue 1"
    )

    valid_party_2: Party = create_party(
        organizer=user,
        party_date=today + dt.timedelta(days=30),
        venue="Venue 2",
    )

    create_party(organizer=other_user, venue="Venue 3")

    create_party(
        organizer=user, party_date=today - dt.timedelta(days=10), venue="Venue 4"
    )

    url: str = reverse(viewname="page_party_list")
    response: HttpResponse = authenticated_client(user).get(url)
    parties_list: list = list(response.context_data["parties"])

    assert response.status_code == 200
    assert len(parties_list) == 2
    assert parties_list == [valid_party_1, valid_party_2]


def test_party_list_page_returns_paginated_list_of_parties(
    authenticated_client: Client,
    create_user: Callable,
    create_party: Callable,
    django_user_model: User,
):
    today: dt.date = dt.date.today()

    for n in range(PartyListPage.paginate_by + 1):
        create_party(
            organizer=create_user,
            party_date=today + dt.timedelta(days=n),
            venue=f"venue {n}",
        )

    url: str = reverse(viewname="page_party_list")
    client: Client = authenticated_client(create_user)

    response: HttpResponse = client.get(url)

    assert response.context["is_paginated"] is True
    assert response.context["page_obj"].has_next() is True
    assert len(list(response.context["parties"])) == PartyListPage.paginate_by

    response = client.get(f"{url}?page=2")
    assert response.context["page_obj"].has_previous() is True
    assert len(list(response.context["parties"])) == 1


def test_party_list_page_returns_different_template_for_htmx_request(
    authenticated_client: Client, create_user: Callable
):
    url: str = reverse(viewname="page_party_list")
    client: Client = authenticated_client(create_user)

    response: HttpResponse = client.get(url)
    assert response.template_name[0] == "party/party_list/page_parties_list.html"

    response = client.get(url, HTTP_HX_REQUEST="")
    assert response.template_name[0] == "party/party_list/partial_parties_list.html"
