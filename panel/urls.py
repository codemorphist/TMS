from django.urls import path

from panel.views import *

app_name = 'panel'
urlpatterns = [
    path('', PanelView.as_view(), name='panel'),
]



