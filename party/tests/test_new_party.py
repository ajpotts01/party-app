# Standard lib imports
from typing import Callable

# Third-party imports
import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

# Project imports
from party.forms import DATE_PAST_ERROR_MESSAGE, INVITATION_ERROR_MESSAGE
from party.models import Party

@pytest.mark.django_db
def test_create_party(
    authenticated_client: Client,
    create_user: Callable,
):
    url: str = reverse(viewname="page_new_party")
    data: dict = {
        "party_date": "2025-06-06",
        "party_time": "18:00:00",
        "venue": "My Venue",
        "invitation": "Come to my party!",
    }

    response: HttpResponse = authenticated_client(create_user).post(url, data)

    assert response.status_code == 302
    assert Party.objects.count() == 1

def test_create_party_invitation_too_short_returns_error(
    authenticated_client: Client, 
    create_user: Callable,
):
    url: str = reverse(viewname="page_new_party")
    data: dict = {
        "party_date": "2025-06-06",
        "party_time": "18:00:00",
        "venue": "My Venue",
        "invitation": "Too short",
    }

    response: HttpResponse = authenticated_client(create_user).post(url, data)

    assert not response.context["form"].is_valid()
    assert INVITATION_ERROR_MESSAGE in response.content.decode()
    assert Party.objects.count() == 0

def test_create_party_past_date_returns_error(
    authenticated_client: Client,
    create_user: Callable,
):
    url: str = reverse(viewname="page_new_party")
    data: dict = {
        "party_date": "2020-06-06",
        "party_time": "18:00:00",
        "venue": "My Venue",
        "invitation": "Come to my party!",
    }

    response: HttpResponse = authenticated_client(create_user).post(url, data)

    assert not response.context["form"].is_valid()
    assert DATE_PAST_ERROR_MESSAGE in response.content.decode()
    assert Party.objects.count() == 0

def test_partial_party_check_date(
    authenticated_client: Client,
    create_user: Callable,
):
    url: str = reverse(viewname="partial_check_party_date")
    data: dict = {
        "party_date": "2020-06-06",
    }

    response: HttpResponse = authenticated_client(create_user).get(url, data)

    assert response.status_code == 200
    assert 'id="id_party_date"' in response.content.decode()
    assert DATE_PAST_ERROR_MESSAGE in response.content.decode()

def test_partial_check_invitation(
    authenticated_client: Client,
    create_user: Callable,
):
    url: str = reverse(viewname="partial_check_invitation")
    data: dict = {
        "invitation": "Too short",
    }

    response: HttpResponse = authenticated_client(create_user).get(url, data)

    assert response.status_code == 200
    assert 'id="id_invitation"' in response.content.decode()
    assert INVITATION_ERROR_MESSAGE in response.content.decode()