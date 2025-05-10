from django.urls import path

from users import views
from users.views import PanelUserLoginView, PanelUserLogoutView

app_name = 'users'
urlpatterns = [
    path('login/', PanelUserLoginView.as_view(), name='login'),
    path('logout/', PanelUserLogoutView.as_view(), name='logout'),

    path('register/client/', views.RegisterClient.as_view(), name='register-client'),
    path('register/provider/', views.RegisterProvider.as_view(), name='register-provider'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
]