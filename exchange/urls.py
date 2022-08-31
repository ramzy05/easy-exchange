from django.urls import path
from .views import home_view, create_account_view, signin_view, signout_view, transaction_view, get_users_per_country_view
urlpatterns = [
    path('', home_view, name='home'),
    path('register', create_account_view, name='register'),
    path('login', signin_view, name='login'),
    path('logout', signout_view, name='logout'),
    path('transaction', transaction_view, name='make_transaction'),
    path('users/<str:country>', get_users_per_country_view),
]
