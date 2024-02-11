from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url="login/")
def home(request):
    return render(request, 'home.html')

@login_required(login_url="login/")
def pessoas(request):
    return render(request,'pessoas.html')

def logar(request):
    erro_login = None
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('user'), password=request.POST.get('senha'))
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                return redirect('home')
        else:
            erro_login = 'Credenciais incorretas. Por favor, tente novamente.'
    return render(request, 'login.html', {'erro_login': erro_login})

def deslogar(request):
    logout(request)
    return redirect('login')