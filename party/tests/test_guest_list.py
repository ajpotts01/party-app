# Standard lib imports
from typing import Callable

# Third-party imports
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

# Project imports
from party.models import Guest, Party


def test_page_guest_list_lists_guests_for_certain_party(
    authenticated_client: Client,
    create_user: Callable,
    create_party: Callable,
    create_guest: Callable,
):
    party: Party = create_party(organizer=create_user, venue="Main venue")
    guest_1: Guest = create_guest(party=party, name="Anna Brown")
    guest_2: Guest = create_guest(party=party, name="Lia Keyes")

    another_party: Party = create_party(organizer=create_user, venue="Another venue")
    create_guest(party=another_party, name="Guest from another party")

    url = reverse("page_guest_list", args=[party.uuid])

    response: HttpResponse = authenticated_client(create_user).get(url)
    response_guests_list: list = list(response.context["guests"])

    assert response.status_code == 200
    assert response.context["party_id"] == party.uuid
    assert response_guests_list == [guest_1, guest_2]
    assert len(response_guests_list) == 2


def test_mark_guest_attending(
    authenticated_client: Client,
    create_user: Callable,
    create_party: Callable,
    create_guest: Callable,
):
    party: Party = create_party(organizer=create_user)
    guest_1: Guest = create_guest(party=party, attending=False)
    guest_2: Guest = create_guest(party=party, attending=False)

    url: str = reverse(viewname="partial_mark_attending", args=[party.uuid])

    data: str = f"guest_ids={guest_1.uuid}"
    response: HttpResponse = authenticated_client(create_user).put(
        url, data=data, content_type="application/x-www-form-urlencoded"
    )

    assert Guest.objects.get(uuid=guest_1.uuid).attending is True
    assert Guest.objects.get(uuid=guest_2.uuid).attending is False

    assert response.status_code == 200
    assert len(list(response.context["guests"])) == 2


def test_mark_guest_not_attending(
    authenticated_client: Client,
    create_user: Callable,
    create_party: Callable,
    create_guest: Callable,
):
    party: Party = create_party(organizer=create_user)
    guest_1: Guest = create_guest(party=party, attending=True)
    guest_2: Guest = create_guest(party=party, attending=True)

    url = reverse(viewname="partial_mark_not_attending", args=[party.uuid])

    data: str = f"guest_ids={guest_1.uuid}"
    response: HttpResponse = authenticated_client(create_user).put(
        url, data=data, content_type="application/x-www-form-urlencoded"
    )

    assert Guest.objects.get(uuid=guest_1.uuid).attending is False
    assert Guest.objects.get(uuid=guest_2.uuid).attending is True

    assert response.status_code == 200
    assert len(list(response.context["guests"])) == 2
