# Standard lib imports
import datetime as dt
from typing import Callable

# Third-party imports
import pytest
from django.test import Client
from django.contrib.auth.models import User

# Project imports
from party.models import Party, Gift, Guest, CustomUser


@pytest.fixture(scope="function")
def create_user(django_user_model: User) -> User:
    return django_user_model.objects.create_user(username="testuser", password="123456")

@pytest.fixture(scope="session")
def authenticated_client() -> Callable:
    def _authenticated_client(test_user: CustomUser) -> Client:
        client: Client = Client()
        client.force_login(user=test_user)

        return client
    
    return _authenticated_client

@pytest.fixture(scope="session")
def create_party() -> Callable:
    def _create_party(organizer: CustomUser, **kwargs) -> Party:
        return Party.objects.create(
            organizer=organizer,
            party_date=kwargs.get("party_date", dt.date.today()),
            party_time=kwargs.get("party_time", dt.datetime.now()),
            venue=kwargs.get("venue", "Amazing castle"),
        )
    
    return _create_party

@pytest.fixture(scope="session")
def create_gift() -> Callable:
    def _create_gift(party: Party, **kwargs) -> Gift:
        return Gift.objects.create(
            gift=kwargs.get("gift", "Test gift"),
            price=kwargs.get("price", 12.5),
            link=kwargs.get("link", "https://testlink.com"),
            party=party,
        )
    
    return _create_gift

@pytest.fixture(scope="session")
def create_guest() -> Callable:
    def _create_guest(party: Party, **kwargs):
        return Guest.objects.create(
            name=kwargs.get("name", "John Doe"),
            attending=kwargs.get("attending", True),
            party=party,
        )
    
    return _create_guest