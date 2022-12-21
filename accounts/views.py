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
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import IpAddress

# Restituisce l'attuale IP 
@csrf_exempt
def getActualIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

# Crea l'oggetto IP con la data attuale
@csrf_exempt
def addIp(actualIp):
    ip_address = IpAddress(
        ip_address=actualIp, pub_date=datetime.now())
    ip_address.save()

# View pagina di login
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

# View pagina di registrazione
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

# View di logout
@csrf_exempt
def logoutUser(request):
    logout(request)
    return redirect('login')

# View della pagina con la tabella dati
@csrf_exempt
@login_required(login_url='login')
def consumiPage(request):

    # Quando vede una request POST prende i dati e crea un oggetto nel 
    # db e manda la transazione on chain (VIA POSTMAN)
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        produced_energy_in_watt = body['produced_energy_in_watt']
        consumed_energy_in_watt = body['consumed_energy_in_watt']

        t = Consumi(produced_energy_in_watt=produced_energy_in_watt,
                    consumed_energy_in_watt=consumed_energy_in_watt)
        Consumi.writeOnChain(t)

    # Calcola il totale per mandarlo all'html
    data = Consumi.objects.all()
    totaleP = 0
    totaleC = 0
    for object in data:
        totaleP += int(object.produced_energy_in_watt)
        totaleC += int(object.consumed_energy_in_watt)

    return render(request, 'accounts/consumi.html',  {'data': data, 'totaleP': totaleP, 'totaleC': totaleC})

# View home
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

    return render(request, 'accounts/home.html', checkIp)

# Inserisce nel database i dati che si inseriscono in inser.html nella textarea
def inserData(request):

    # Quando vede una request POST prende i dati e crea un oggetto 
    # nel db e manda la transazione on chain
    if request.method == "POST":
        dati = request.POST.get('dati')
        dati = json.loads(dati)
        print(type(dati))
        produced_energy_in_watt = dati['produced_energy_in_watt']
        consumed_energy_in_watt = dati['consumed_energy_in_watt']

        t = Consumi(produced_energy_in_watt=produced_energy_in_watt,
                    consumed_energy_in_watt=consumed_energy_in_watt)
        Consumi.writeOnChain(t)

        messages.success(request, 'Dati inseriti nel database!')

        return redirect('home')

    context = {}
    return render(request, 'accounts/inser.html', context)
