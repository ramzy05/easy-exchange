from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import random
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, country, password=None):
        if not username:
            raise ValueError('username is required')
        if not first_name:
            raise ValueError('fisrt name is required')
        if not last_name:
            raise ValueError('last name is required')
        if not country:
            raise ValueError('Please choose a country')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            country=country,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, country, password=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            country=country,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(verbose_name=_(
        'username'), max_length=100, unique=True)
    # email = models.EmailField(verbose_name=_('Email adress'), max_length= 68, unique=True)
    first_name = models.CharField(verbose_name=_('first_name'), max_length=100)
    last_name = models.CharField(verbose_name=_('last_name'), max_length=100)
    country = models.CharField(verbose_name=_('country'), max_length=100)
    balance = models.DecimalField(verbose_name=_(
        'balance'), default=5000, max_digits=15, decimal_places=2)
    pin = models.CharField(max_length=4, default='1111')
    date_joined = models.DateTimeField(
        verbose_name=("date_joined"), auto_now_add=True)
    last_login = models.DateTimeField(verbose_name=_(
        'last login'), blank=True, null=True, auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def get_balance(self):
        currency = Country.objects.filter(
            name=self.country).first().currency or 'XAF'
        return f'{currency} {self.balance}'

    @property
    def get_country_currency(self):
        currency = Country.objects.filter(
            name=self.country).first().currency or 'XAF'
        return currency

    @property
    def get_receptions(self):
        return Transaction.objects.filter(receiver=self)

    @property
    def get_fullname(self):
        return self.first_name.capitalize()+' '+self.last_name.capitalize()


class Country(models.Model):
    name = models.CharField(max_length=50)
    currency = models.CharField(max_length=5)


class Transaction(models.Model):
    sender = models.ForeignKey(
        Account, related_name='sender', on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(
        Account, related_name='receiver', on_delete=models.SET_NULL, null=True, blank=True)
    amount_received = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)
    amount_sent = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.sender.username}-{self.created}-{self.receiver.username}'

    @property
    def get_amount_sent(self):
        currency = Country.objects.filter(
            name=self.sender.country).first().currency or 'XAF'
        currency
        return f'{currency} {self.amount_sent}'

    @property
    def get_amount_received(self):
        currency = Country.objects.filter(
            name=self.receiver.country).first().currency or 'XAF'
        currency
        return f'{currency} {self.amount_received}'
