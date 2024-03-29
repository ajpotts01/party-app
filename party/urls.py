# Third-party imports
from django.urls import URLPattern, path

# Project imports
from . import views

list_parties_urlpatterns: list[URLPattern] = [
    path(route="", view=views.PartyListPage.as_view(), name="page_party_list"),
]

party_detail_urlpatterns: list[URLPattern] = [
    path(
        route="party/<uuid:party_uuid>/",
        view=views.PartyDetailPage.as_view(),
        name="page_single_party",
    ),
    path(
        route="party/<uuid:party_uuid>/details/",
        view=views.PartyDetailPartial.as_view(),
        name="partial_party_detail",
    ),
]

new_party_urlpatterns: list[URLPattern] = [
    path(route="party/new/", view=views.page_new_party, name="page_new_party"),
    path(
        route="party/new/check-date/",
        view=views.partial_check_party_date,
        name="partial_check_party_date",
    ),
    path(
        route="party/new/check-invitation/",
        view=views.partial_check_invitation,
        name="partial_check_invitation",
    ),
]

gift_registry_urlpatterns: list[URLPattern] = [
    path(
        route="party/<uuid:party_uuid>/gifts/",
        view=views.GiftRegistryPage.as_view(),
        name="page_gift_registry",
    ),
    path(
        route="gifts/<uuid:gift_uuid>/",
        view=views.GiftDetailPartial.as_view(),
        name="partial_gift_detail",
    ),
    path(
        route="gifts/<uuid:gift_uuid>/form/",
        view=views.GiftUpdateFormPartial.as_view(),
        name="partial_gift_update",
    ),
    path(
        route="gifts/<uuid:gift_uuid>/delete/",
        view=views.delete_gift_partial,
        name="partial_gift_delete",
    ),
    path(
        route="party/<uuid:party_uuid>/new-gift/",
        view=views.GiftCreateFormPartial.as_view(),
        name="partial_new_gift",
    ),
]

guest_list_patterns: list[URLPattern] = [
    path(
        route="party/<uuid:party_uuid>/guests/",
        view=views.GuestListPage.as_view(),
        name="page_guest_list",
    ),
    path(
        route="party/<uuid:party_uuid>/guests/mark-attending/",
        view=views.mark_attending_partial,
        name="partial_mark_attending",
    ),
    path(
        route="party/<uuid:party_uuid>/guests/mark-not-attending/",
        view=views.mark_not_attending_partial,
        name="partial_mark_not_attending",
    ),
    path(
        route="party/<uuid:party_uuid>/guests/filter/",
        view=views.filter_guests_partial,
        name="partial_filter_guests",
    ),
]

general_patterns: list[URLPattern] = [
    path(route="login/", view=views.LoginPage.as_view(), name="party_login"),
]

urlpatterns: list[URLPattern] = (
    general_patterns
    + list_parties_urlpatterns
    + party_detail_urlpatterns
    + new_party_urlpatterns
    + gift_registry_urlpatterns
    + guest_list_patterns
)
