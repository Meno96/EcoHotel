from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from .models import Consumi
import json

# from tkinter import *
import tkinter as tk
import tkinter.messagebox

# Create your views here.
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import IpAddress


def messageBox(message):
    root = tk.Tk()
    label = tk.Label(root, text=message)
    label.pack(side="top", fill="both", expand=True, padx=20, pady=20)
    button = tk.Button(root, text="OK", command=lambda: root.destroy())
    button.pack(side="bottom", fill="none", expand=True)
    root.mainloop()


@csrf_exempt
def getActualIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


@csrf_exempt
def addIp(actualIp):
    ip_address = IpAddress(
        ip_address=actualIp, pub_date=datetime.now())
    ip_address.save()


@unauthenticated_user
@csrf_exempt
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username o Password sono sbagliati')

    return render(request, 'accounts/login.html')


@unauthenticated_user
@csrf_exempt
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account a nome ' +
                             username + ' è stato creato!')
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@csrf_exempt
def logoutUser(request):
    logout(request)
    return redirect('login')


@csrf_exempt
@login_required(login_url='login')
def consumiPage(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        produced_energy_in_watt = body['produced_energy_in_watt']
        consumed_energy_in_watt = body['consumed_energy_in_watt']

        # print(body)
        t = Consumi(produced_energy_in_watt=produced_energy_in_watt,
                    consumed_energy_in_watt=consumed_energy_in_watt)
        Consumi.writeOnChain(t)

        # return JsonResponse(t, safe=False)

    data = Consumi.objects.all()
    totaleP = 0
    totaleC = 0
    for object in data:
        totaleP += int(object.produced_energy_in_watt)
        totaleC += int(object.consumed_energy_in_watt)

    return render(request, 'accounts/consumi.html',  {'data': data, 'totaleP': totaleP, 'totaleC': totaleC})


@csrf_exempt
def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@csrf_exempt
def homePage(request):

    # Memorizza l’ultimo IP che ha avuto accesso alla
    # piattaforma per un admin, mostra un messaggio di
    # avvertimento quando questo è diverso dal precedente
    checkIp={'checkIp': None}
    if request.user.is_staff:
        dbIp = IpAddress.objects.all().values().last()
        actualIp = getActualIP(request)

        if not dbIp:
            addIp(actualIp)
        else:
            if actualIp != dbIp['ip_address']:
                addIp(actualIp)
                checkIp={'checkIp': True}
                # messageBox(
                #     "L'indirizzo IP corrente è diverso dal precedente con cui è stato effettuato il login!")
    
    print(checkIp)

    return render(request, 'accounts/home.html', checkIp)
