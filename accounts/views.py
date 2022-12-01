from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only

@csrf_exempt
def accountsPage(request):
    context = {}
    return render(request, 'accounts/accounts.html', context)


@unauthenticated_user
@csrf_exempt
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username o Password sono sbagliati')

    context = {}
    return render(request, 'accounts/login.html', context)


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
@admin_only
def consumiPage(request):
    context = {}
    return render(request, 'accounts/consumi.html', context)
@csrf_exempt
def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)
