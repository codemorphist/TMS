from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def panel(request: HttpRequest) -> HttpResponse:
    """
    View for home page of panel
    """
    return render(request, 'panel/panel.html')


