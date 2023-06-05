from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Vous êtes connecté avec succès !')
            return redirect('dashboard')  # Rediriger vers le tableau de bord après la connexion
        else:
            messages.error(request, 'Identifiants invalides')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')


def dashboard(request):
    """ view du tableau de bord"""
    return render(request, 'dashboard.html')
