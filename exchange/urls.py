from django.urls import path
from .views import home_view, registration_view, signin_view, signout_view, transaction_view, get_users_per_country_view, welcome_view, history_view
urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('home', home_view, name='home'),
    path('history', history_view, name='history'),
    path('register', registration_view, name='register'),
    path('login', signin_view, name='login'),
    path('logout', signout_view, name='logout'),
    path('transaction', transaction_view, name='make_transaction'),
    path('users/<str:country>', get_users_per_country_view),
]
