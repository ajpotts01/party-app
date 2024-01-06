# Standard lib imports
from typing import Callable

# Third-party imports
import pytest
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
    assert response.context["party_id"] == party.uuid


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
    assert response.context["party_id"] == party.uuid


@pytest.mark.parametrize(
    "guest_attending_status, search_text, attending_filter, expected_number_of_filtered_guests",
    [
        (True, "an", "all", 1),  # should pass, this is the same as before
        (True, "be", "all", 0),  # should pass, this is the same as before
        (True, "be", "attending", 0),  # should pass since search doesn't match
        (True, "be", "not_attending", 0),  # should pass since search doesn't match
        (
            True,
            "an",
            "attending",
            1,
        ),  # should pass since search matches and status isn't checked
        (
            True,
            "an",
            "not_attending",
            0,
        ),  # should fail since search matches but filter doesn't
        (True, "", "attending", 1),  # should pass since empty search matches the result
        (
            True,
            "",
            "not_attending",
            0,
        ),  # should fail, since search matches, but filter doesn't
        (False, "an", "all", 1),  # should pass since filter is "all"
        (False, "be", "all", 0),  # should pass since filter is "all"
        (False, "be", "attending", 0),  # should pass since search doesn't match
        (False, "be", "not_attending", 0),  # should pass since search doesn't match
        (
            False,
            "an",
            "attending",
            0,
        ),  # should fail since "an" matches, but "attending" shouldn't
        (
            False,
            "an",
            "not_attending",
            1,
        ),  # should pass since filter matches even if not checked
        (False, "", "attending", 0),  # should fail since filter doesn't match output
        (
            False,
            "",
            "not_attending",
            1,
        ),  # should pass since filter matches output even if not checked
    ],
)
def test_filter_guests_by_status_and_search(
    guest_attending_status: bool,
    search_text: str,
    attending_filter: str,
    expected_number_of_filtered_guests: int,
    authenticated_client: Client,
    create_user: Callable,
    create_party: Callable,
    create_guest: Callable,
):
    party: Party = create_party(organizer=create_user)

    create_guest(party=party, name="Anna", attending=guest_attending_status)

    url: str = reverse(viewname="partial_filter_guests", args=[party.uuid])
    data: dict = {
        "attending_filter": attending_filter,
        "guest_search": search_text,
    }

    response: HttpResponse = authenticated_client(create_user).post(url, data)

    assert len(list(response.context["guests"])) == expected_number_of_filtered_guests
