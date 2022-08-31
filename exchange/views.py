from django.core.exceptions import ValidationError
import json
from django.shortcuts import render, redirect
from .forms import CreateAccountForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Account, Country, Transaction
from django.http.response import JsonResponse
from django.conf import settings


def home_view(request):

  context = {}
  return render(request, 'exchange/home.html', context)


def create_account_view(request):
  if request.user.is_authenticated:
    return redirect('home')
  form = CreateAccountForm()
  if request.method == 'POST':
    form = CreateAccountForm(request.POST)
    if form.is_valid():
      form.save()
      return JsonResponse({'result': True}, safe=False, status=201)
    else:
      print(form.errors.as_json())
      return JsonResponse({'result': False, 'errors': json.loads(form.errors.as_json())}, safe=False, status=400)
  context = {
      'form': form,
  }
  return render(request, 'exchange/signup.html', context)


def signin_view(request):
  pass


def signin_view(request):
  if request.user.is_authenticated:
    return redirect('home')
  form = CreateAccountForm()
  if request.method == 'POST':
    form = CreateAccountForm(request.POST)
    username = form['username'].value()
    password = form['password1'].value()
    if username == '':
      return JsonResponse({'result': False, 'errors': {'username': [{'message': 'This field cannot be blank'}]}}, status=400, safe=False)

    if password == '':
      return JsonResponse({'result': False, 'errors': {'password1': [{'message': 'This field cannot be blank'}]}}, status=400, safe=False)

    if not Account.objects.filter(username=username).exists():
      return JsonResponse({'result': False, 'errors': {'username': [{'message': 'User not found, enter another username'}]}}, status=400, safe=False)

    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
      login(request, user)
      return JsonResponse({'result': True}, status=200, safe=False)
    else:
      return JsonResponse({'result': False, 'errors': {'password1': [{'message': 'Invalid password'}]}}, status=400, safe=False)

  context = {
      'form': form,
  }
  return render(request, 'exchange/signin.html', context)


@login_required(login_url='login')
def signout_view(request):
  logout(request)
  return redirect('home')


@login_required(login_url='login')
def transaction_view(request):
  countries = Country.objects.all()
  context = {'countries': countries, }
  return render(request, 'exchange/transaction.html',  context)


def get_users_per_country_view(request, country):
  if country == '':
    return JsonResponse({'result:': False, 'users': [], 'currency': ''}, safe=False, status=400)

  users = Account.objects.filter(country=country)
  users = [{'username': user.username, 'first_name': user.first_name,
            'last_name': user.last_name} for user in users]
  currency = Country.objects.get(name=country).currency or ''
  return JsonResponse({'result:': True, 'users': users, 'currency': currency}, safe=False, status=200)
