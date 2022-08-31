from django.contrib import admin
from .models import Transaction, Account, Country


# admin.site.register([Account])
admin.site.register([Account, Transaction, Country])
