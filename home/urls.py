from django.urls import path

import home.views as views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
]
