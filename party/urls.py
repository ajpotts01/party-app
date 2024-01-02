# Third-party imports
from django.urls import URLPattern, path

# Project imports
from . import views

list_parties_urlpatterns: list[URLPattern] = [
    path(route="", view=views.PartyListPage.as_view(), name="page_party_list"),
]

party_detail_urlpatterns: list[URLPattern] = [
    path(route="party/<uuid:party_uuid>/", view=views.PartyDetailPage.as_view(), name="page_single_party"),
    path(route="party/<uuid:party_uuid>/details/", view=views.PartyDetailPartial.as_view(), name="partial_party_detail"),
]

urlpatterns: list[URLPattern] = list_parties_urlpatterns + party_detail_urlpatterns