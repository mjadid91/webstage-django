from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def connexion(request):
    if request.method == "POST":
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        
        user = authenticate(request, username=usr, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('main')   # Redirection vers la page d'accueil
        else:
            return render(request, 'appcompte/login.html', {'error': True})

    return render(request, 'appcompte/login.html')


def deconnexion(request):
    logout(request)
    return redirect('login')

def formulaireInscription(request):
    return render(request, "appcompte/formulaireInscription.html")

def traitementFormulaireInscription(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    login(request, user)

    return redirect("/offres/")

def mon_compte(request):
    return render(request, "appcompte/mon_compte.html")