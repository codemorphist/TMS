from django.urls import path

import panel.views as views

urlpatterns = [
    path('', views.panel)
]


