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
