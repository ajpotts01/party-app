# Third-party imports
from django.urls import URLPattern, path

# Project imports
from . import views

list_parties_urlpatterns: list[URLPattern] = [
    path(route="", view=views.PartyListPage.as_view(), name="page_party_list"),
]

urlpatterns: list[URLPattern] = list_parties_urlpatterns