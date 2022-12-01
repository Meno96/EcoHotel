from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .forms import CreateUserForm


def accountsPage(request):
    context = {}
    return render(request, 'accounts/accounts.html', context)


def loginPage(request):
    context = {}
    return render(request, 'accounts/login.html', context)

@csrf_exempt
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/register.html', context)


def consumiPage(request):
    context = {}
    return render(request, 'accounts/consumi.html', context)
