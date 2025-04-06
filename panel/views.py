from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def panel(request: HttpRequest) -> HttpResponse:
    return render(request, 'panel/panel.html')


