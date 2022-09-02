import json
from django.shortcuts import render, redirect
from .forms import CreateAccountForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Account, Country, Transaction
from django.http.response import JsonResponse
from django.db.models import Q
import decimal


def welcome_view(request):
    context = {}
    return render(request, 'exchange/index.html', context)


@login_required(login_url='login')
def home_view(request):
    user = request.user
    transactions = Transaction.objects.filter(Q(sender=user) | Q(receiver=user)
                                              )
    # to get index for the table
    transactions = [[i+1, t] for i, t in enumerate(transactions)]
    context = {'transactions': transactions}
    return render(request, 'exchange/home.html', context)


def registration_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateAccountForm()
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'result': True, 'url': '/login'}, safe=False, status=201)
        else:
            return JsonResponse({'result': False, 'errors': json.loads(form.errors.as_json())}, safe=False, status=400)
    context = {
        'form': form,
    }
    return render(request, 'exchange/signup.html', context)


def signin_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateAccountForm()

    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        username = form['username'].value()
        password = form['password1'].value()
        if username == '':
            return JsonResponse({'result': False, 'errors': {'username': [{'message': 'Username cannot be blank'}]}}, status=400, safe=False)

        if password == '':
            return JsonResponse({'result': False, 'errors': {'password1': [{'message': 'Password field cannot be blank'}]}}, status=400, safe=False)

        if not Account.objects.filter(username=username).exists():
            return JsonResponse({'result': False, 'errors': {'username': [{'message': 'User not found, enter another username'}]}}, status=400, safe=False)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return JsonResponse({'result': True, 'url': '/home'}, status=200, safe=False)
        else:
            return JsonResponse({'result': False, 'errors': {'password1': [{'message': 'Invalid password'}]}}, status=400, safe=False)

    context = {
        'form': form,
    }
    return render(request, 'exchange/signin.html', context)


@login_required(login_url='login')
def signout_view(request):
    logout(request)
    return redirect('welcome')


@login_required(login_url='login')
def transaction_view(request):
    user = request.user
    countries = Country.objects.all()
    context = {'countries': countries}

    if request.method == 'POST':
        user_pin_code = request.POST['pin_code']
        withdraw_amount = decimal.Decimal(request.POST['amount'])
        received_amount = decimal.Decimal(request.POST['amount_converted'])

        if user_pin_code != user.pin:
            return JsonResponse({'result': False, 'errors': {'code_pin': [{'message': 'Your pin code is incorrect'}]}}, safe=False, status=400)
        receiver = Account.objects.get(
            username=request.POST['receiver']) or None

        if receiver is None:
            return JsonResponse({'result': False, 'errors': {'receiver': [{'message': 'Unkwown receiver'}]}}, safe=False, status=400)
        # Everything is good we can make the transaction between the too user
        user.balance -= withdraw_amount
        receiver.balance += received_amount
        user.save(update_fields=['balance'])
        receiver.save(update_fields=['balance'])
        new_transaction = Transaction.objects.create(
            sender=user, receiver=receiver, amount_sent=withdraw_amount, amount_received=received_amount)
        if new_transaction:
            return JsonResponse({'result': True, 'url': '/home'}, safe=False, status=201)

        return JsonResponse({'result': False, 'errors': 'server internal error'}, safe=False, status=500)

    return render(request, 'exchange/transaction.html',  context)


def get_users_per_country_view(request, country):
    if country == ' ':
        return JsonResponse({'result:': False, 'users': [], 'currency': ''}, safe=False, status=400)

    users = Account.objects.filter(country=country).exclude(
        username=request.user.username)

    users = [{'username': user.username, 'first_name': user.first_name,
              'last_name': user.last_name} for user in users]

    currency = Country.objects.get(name=country).currency or ''
    return JsonResponse({'result:': True, 'users': users, 'currency': currency}, safe=False, status=200)


@login_required(login_url='login')
def history_view(request):
    user = request.user

    transactions = Transaction.objects.filter(Q(sender=user) | Q(receiver=user)
                                              )
    transactions = [[i+1, t] for i, t in enumerate(transactions)]
    # in the templates i is going to be the index in the table
    context = {'transactions': transactions}
    return render(request, 'exchange/history.html', context)
