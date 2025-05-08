from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/home.html')
