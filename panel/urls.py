from django.urls import path

import panel.views as views

app_name = 'panel'
urlpatterns = [
    path('', views.PanelView.as_view(), name='panel'),
]



