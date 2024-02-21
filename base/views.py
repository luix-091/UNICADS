from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Pessoa, Endereco
from .forms import PessoaForm, EnderecoForm
from datetime import datetime

# Create your views here.
@login_required(login_url="login/")
def home(request):
    return render(request, 'home.html')

@login_required(login_url="login/")
def pessoas(request):
    pessoas = Pessoa.objects.all()
    pesquisa = request.GET.get('pesquisa')

    if pesquisa:
        pessoas = pessoas.filter(
            Q(nome__icontains=pesquisa) | 
            Q(cpf__icontains=pesquisa) | 
            Q(data_nasc__icontains=pesquisa) |
            Q(enderecos__logradouro__icontains=pesquisa) |
            Q(enderecos__regiao__icontains=pesquisa) |
            Q(enderecos__bairro__icontains=pesquisa)
        )
    for pessoa in pessoas:
        data_nasc_formatada = pessoa.data_nasc.strftime('%d/%m/%Y')
        pessoa.data_nasc = datetime.strptime(data_nasc_formatada, '%d/%m/%Y')
    return render(request, 'pessoas.html', {'pessoas':pessoas})

@login_required(login_url='login/')
def cad_pessoa(request):
    if request.method == 'POST':
        form_pessoa = PessoaForm(request.POST)
        form_endereco = EnderecoForm(request.POST)
        if form_pessoa.is_valid() and form_endereco.is_valid():
            endereco = form_endereco.save()
            pessoa = form_pessoa.save(commit=False)
            pessoa.enderecos = endereco
            pessoa.save()
            return redirect('pessoas')
    bairros = [bairro[0] for bairro in Endereco.BAIRROS_CHOICES]
    return render(request, 'cadastro.html', {'bairros': bairros})


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
    
    bairros = [bairro[0] for bairro in Endereco.BAIRROS_CHOICES]
    form_pessoa = PessoaForm(request.POST, instance=pessoa)
    form_endereco = EnderecoForm(request.POST, instance=pessoa.enderecos)
    return render(request, 'editar.html', {'form_pessoa': form_pessoa, 'form_endereco': form_endereco, 'pessoa': pessoa, 'bairros':bairros})

@login_required(login_url='login/')
def relatorios(request):

    pessoas = Pessoa.objects.all()
    total_pessoas = '{:,}'.format(Pessoa.objects.all().count()).replace(',', '.')

    bairros = [bairro[0] for bairro in Endereco.BAIRROS_CHOICES]

    selected_bairros = request.GET.getlist('bairros')


    if not selected_bairros:
        selected_bairros = ''
    
    return render(request, 'relatorios.html', {'pessoas':pessoas, 'total_pessoas':total_pessoas, 'bairros':bairros, 'selected_bairros':selected_bairros})



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