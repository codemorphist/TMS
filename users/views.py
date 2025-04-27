from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from users.forms import PanelUserCreationForm


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PanelUserCreationForm(request.POST)
    else:
        form = PanelUserCreationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)