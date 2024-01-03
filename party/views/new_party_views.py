# Third-party imports
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from party.forms import PartyForm
from party.models import Party


@login_required
def page_new_party(request: HttpRequest) -> HttpResponse:
    form: PartyForm = PartyForm()

    if request.method == "POST":
        form = PartyForm(request.POST)
        if form.is_valid():
            party: Party = form.save(commit=False)
            party.organizer = request.user
            party.save()
            return redirect(to="page_single_party", party_uuid=party.uuid)
    
    return render(request=request, template_name="party/new_party/page_new_party.html", 
                  context={
                      "form": form,
                  })

@login_required
def partial_check_party_date(request: HttpRequest) -> HttpResponse:
    form: PartyForm = PartyForm(data=request.GET)

    return HttpResponse(content=as_crispy_field(field=form["party_date"]))

@login_required
def partial_check_invitation(request: HttpRequest) -> HttpResponse:
    form: PartyForm = PartyForm(data=request.GET)

    return HttpResponse(content=as_crispy_field(field=form["invitation"]))