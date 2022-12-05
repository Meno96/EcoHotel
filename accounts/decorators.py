from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

# Se l'user è autenticato lo reindirizza alla home sennò continua la funzione
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

# Se l'utente non ha i permessi non viene mostrata la pagina 
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Non sei autorizzato a vedere questa pagina.')

        return wrapper_func
    return decorator

# Permette l'accesso solo agli utenti del gruppo admin
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func
