from django.urls import path
from .views import home_view, create_account_view, signin_view, signout_view
urlpatterns = [
    path('', home_view, name='home'),
    path('register', create_account_view, name='register'),
    path('login', signin_view, name='login'),
    path('logout', signout_view, name='logout'),
]
