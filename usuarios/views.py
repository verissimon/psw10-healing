from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponse

def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(request, constants.ERROR, "Usuário já existe")
            return redirect(reverse("login"))

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, "Senhas não conferem")
            return redirect(reverse("cadastro"))

        if len(senha) < 8:
            messages.add_message(
                request, constants.ERROR, "Senha deve ter no mínimo 8 caracteres"
            )
            return redirect(reverse("cadastro"))

        try:
            User.objects.create_user(username=username, email=email, password=senha)
            messages.add_message(
                request, constants.SUCCESS, "Usuário cadastrado com sucesso"
            )
            return redirect(reverse("login"))

        except Exception as e:
            messages.add_message(
                request, constants.ERROR, f"Erro ao cadastrar usuário. {e}"
            )
            return redirect(reverse("cadastro"))

def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    if request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            # TODO /pacientes/home
            # return redirect(reverse('home')) 
            return redirect(reverse('login'))
        
        messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
        return redirect(reverse('login'))

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))