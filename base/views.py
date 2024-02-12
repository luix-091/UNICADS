from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Pessoa, Endereco
from .forms import PessoaForm, EnderecoForm

# Create your views here.
@login_required(login_url="login/")
def home(request):
    return render(request, 'home.html')

@login_required(login_url="login/")
def pessoas(request):
    pessoas = Pessoa.objects.all()
    return render(request, 'pessoas.html', {'pessoas':pessoas})

@login_required(login_url="login/")
def apagar_pessoa(request, pessoa_id):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    if request.method == 'POST':
        pessoa.delete()
    return redirect('pessoas')

@login_required(login_url='login/')
def editar_pessoa(request, pessoa_id):
    pessoa = Pessoa.objects.get(id=pessoa_id)
    if request.method == 'POST':
        form_pessoa = PessoaForm(request.POST, instance=pessoa)
        form_endereco = EnderecoForm(request.POST, instance=pessoa.enderecos)
        if form_pessoa.is_valid() and form_endereco.is_valid():
            form_pessoa.save()
            form_endereco.save()
            return redirect('pessoas')
    form_pessoa = PessoaForm(request.POST, instance=pessoa)
    form_endereco = EnderecoForm(request.POST, instance=pessoa.enderecos)
    return render(request, 'editar.html', {'form_pessoa': form_pessoa, 'form_endereco': form_endereco, 'pessoa': pessoa})

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